from agent.mappers.search_mapper import map_search_output
from agent.mappers.booking_mapper import map_booking_output
from agent.mappers.transfer_mapper import map_service_output

# Tool adına göre doğru mapper'ı döner
MAPPER_REGISTRY: dict = {
    "search_rooms": map_search_output,
    "create_booking": map_booking_output,
    "add_service": map_service_output,
}

__all__ = ["MAPPER_REGISTRY"]
