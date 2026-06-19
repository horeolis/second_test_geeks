import flet as ft
from db import main_db


def main_page(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = "dark"

    item_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)
    counter_text = ft.Text(value="Куплено: 0", size=16)

    filter_type = "all"

    def update_counter():
        purchased_count = len([1 for _, _, _, p in main_db.get_tasks(filter_type="completed")])
        counter_text.value = f"Куплено: {purchased_count}"

    def load_items():
        item_list.controls.clear()
        for item_id, name, quantity, purchased in main_db.get_tasks(filter_type=filter_type):
            item_list.controls.append(view_item(item_id=item_id, name=name, quantity=quantity, purchased=purchased))
        update_counter()

    def view_item(item_id, name, quantity, purchased=None):
        item_field = ft.TextField(value=name, expand=True, read_only=True)
        qty_field = ft.TextField(value=str(quantity), width=50, read_only=True)

        checkbox = ft.Checkbox(
            value=bool(purchased),
            on_change=lambda e: toggle_item(item_id=item_id, is_purchased=e.control.value)
        )

        def delete_item(_):
            main_db.delete_task_db(item_id)
            item_list.controls.remove(row)
            update_counter()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, on_click=delete_item, icon_color="red")

        row = ft.Row([checkbox, item_field, qty_field, delete_button])
        return row

    item_input = ft.TextField(label="Новый товар", expand=True)
    qty_input = ft.TextField(label="Кол-во", width=80, value="1")
    add_button = ft.IconButton(icon=ft.Icons.ADD)

    def toggle_item(item_id, is_purchased):
        main_db.update_task(task_id=item_id, completed=int(is_purchased))
        load_items()

    def add_item(_):
        if item_input.value and item_input.value.strip():
            item_name = item_input.value.strip()
            qty = int(qty_input.value) if qty_input.value.isdigit() else 1
            main_db.add_task_db(task=item_name, quantity=qty)
            item_input.value = ""
            qty_input.value = "1"
            load_items()

    item_input.on_submit = add_item
    add_button.on_click = add_item

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_items()

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все', on_click=lambda e: set_filter('all')),
        ft.ElevatedButton('Не куплены', on_click=lambda e: set_filter('uncompleted')),
        ft.ElevatedButton('Куплены', on_click=lambda e: set_filter('completed'))
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    input_row = ft.Row([item_input, qty_input, add_button])
    page.add(counter_text, input_row, filter_buttons, item_list)
    load_items()


if __name__ == "__main__":
    main_db.init_db()
    ft.app(target=main_page)