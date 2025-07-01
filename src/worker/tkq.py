from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, provide, Scope, make_async_container
from dishka.integrations.taskiq import setup_dishka
from taskiq import TaskiqScheduler, SmartRetryMiddleware
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_nats import NATSKeyValueScheduleSource, PullBasedJetStreamBroker, NATSObjectStoreResultBackend

from src.bot.di import InfrastructureProvider, ConfigurationProvider
from src.configuration import Configuration, NATSConfig


class BotProvider(Provider):
    @provide(scope=Scope.APP)
    def get_bot(self, conf: Configuration) -> Bot:
        return Bot(
            token=conf.bot.token,
            default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
            )
        )


container = make_async_container(
    BotProvider(),
    ConfigurationProvider(),
    InfrastructureProvider(),
)

nats_conf = NATSConfig()

broker = PullBasedJetStreamBroker(servers=[nats_conf.nats_uri,]).with_result_backend(
    NATSObjectStoreResultBackend(
        servers=[
            nats_conf.nats_uri,
        ],
    )).with_middlewares(
        SmartRetryMiddleware(
            default_retry_count=3,
            use_delay_exponent=True,
            max_delay_exponent=120,
            default_delay=3,
            use_jitter=True,
        )
)
schedule_source = NATSKeyValueScheduleSource(servers=[nats_conf.nats_uri,])
scheduler = TaskiqScheduler(
    broker=broker,
    sources=[
        schedule_source,
        LabelScheduleSource(broker=broker)
    ]
)
setup_dishka(container=container, broker=broker)

