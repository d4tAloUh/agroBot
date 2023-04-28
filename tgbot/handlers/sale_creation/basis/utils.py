from tgbot.handlers.sale_creation.city.utils import get_choose_city_callback_data
from tgbot.handlers.sale_creation.region.utils import get_choose_region_callback_data
from tgbot.handlers.sale_creation.subregion.utils import get_choose_subregion_callback_data
from tgbot.handlers.sale_creation.basis import static_text


def get_go_back_from_basis_callback_data(context):
    if not context.user_data.get("region_id"):
        return get_choose_region_callback_data(page=1), static_text.go_back_to_choose_region
    if not context.user_data.get("subregion_id"):
        return get_choose_subregion_callback_data(page=1), static_text.go_back_to_choose_subregion
    return get_choose_city_callback_data(page=1), static_text.go_back_to_choose_city



