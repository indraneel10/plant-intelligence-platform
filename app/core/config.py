from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Plant Intelligence Platform"
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///./data/plant_intelligence.db"
    image_dir: str = "./data/images"
    model_dir: str = "./data/models"
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    hardware_mode: str = "mock"
    mqtt_sensor_topic: str = "plant/sensors"
    mqtt_actuator_topic: str = "plant/actuators/command"
    capture_interval_hours: int = 48
    ai_model: str = "gpt-5.6-luna"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)

settings = Settings()
