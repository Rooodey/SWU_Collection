import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, \
    QHBoxLayout, QLineEdit, QDialog, QFormLayout, QCheckBox, QLabel, QComboBox, QDialogButtonBox
from PyQt6.QtCore import Qt
from services import CardService, PriceService, UserService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas


class DatabaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.card_value = None
        self.filter_input = None
        self.setWindowTitle('SW-Unlimited Database')
        self.setGeometry(100, 100, 800, 600)
        self.table = QTableWidget()
        self.card_service = CardService()
        self.price_service = PriceService()
        self.user_service = UserService()

        self.init_ui()
        self.show_data()

    def init_ui(self):
        layout = QHBoxLayout()

        self.table.setColumnCount(13)
        self.table.setHorizontalHeaderLabels(["Id", "Set", "Nummer", "Variante", "Foil", "Name", "Titel",
                                              "Seltenheit", "Typ", "Link", "7-Tage", "Anzahl", "Details"])
        self.table.setColumnHidden(0, True)
        self.table.setSortingEnabled(True)
        self.table.itemChanged.connect(self.update_data)

        button_layout = QVBoxLayout()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Suche nach Name...")
        self.filter_input.textChanged.connect(self.filter_table)
        self.filter_input.setMaximumWidth(200)
        button_layout.addWidget(self.filter_input)

        self.user_filter = QComboBox()
        user = self.user_service.get_users()
        self.user_filter.addItems(user)
        self.user_filter.currentIndexChanged.connect(self.show_data)
        button_layout.addWidget(self.user_filter)

        self.set_filter = QComboBox()
        sets = ["Alle Sets", "SOR"]
        self.set_filter.addItems(sets)
        self.set_filter.currentIndexChanged.connect(self.filter_table)
        button_layout.addWidget(self.set_filter)

        self.variant_filter = QComboBox()
        variants = ["Alle Varianten", "Normal", "Hyperspace", "Showcase"]
        self.variant_filter.addItems(variants)
        self.variant_filter.currentIndexChanged.connect(self.filter_table)
        button_layout.addWidget(self.variant_filter)

        self.foil_filter = QComboBox()
        foils = ["Foil & Non-foil", "Foil", "Non-foil"]
        self.foil_filter.addItems(foils)
        self.foil_filter.currentIndexChanged.connect(self.filter_table)
        button_layout.addWidget(self.foil_filter)

        self.rarity_filter = QComboBox()
        rarities = ["Alle Seltenheiten", "Rare", "Legendary", "Special"]
        self.rarity_filter.addItems(rarities)
        self.rarity_filter.currentIndexChanged.connect(self.filter_table)
        button_layout.addWidget(self.rarity_filter)

        self.owned_filter = QComboBox()
        owned = ["Alle Karten", "Eigene Karten"]
        self.owned_filter.addItems(owned)
        self.owned_filter.currentIndexChanged.connect(self.filter_table)
        button_layout.addWidget(self.owned_filter)

        button_layout.addStretch(1)

        btn_add_card = QPushButton('Add Card')
        btn_add_card.clicked.connect(self.add_card)
        button_layout.addWidget(btn_add_card)

        btn_add_user = QPushButton('Add User')
        btn_add_user.clicked.connect(self.add_user)
        button_layout.addWidget(btn_add_user)

        btn_delete = QPushButton('Delete')
        btn_delete.clicked.connect(self.delete_data)
        button_layout.addWidget(btn_delete)

        button_layout.addStretch(1)

        self.card_value = QLabel("Kartenwert: ")
        button_layout.addWidget(self.card_value)

        layout.addWidget(self.table)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def filter_table(self):
        filter_text = self.filter_input.text().strip().lower()
        selected_set = self.set_filter.currentText()
        selected_variant = self.variant_filter.currentText()
        selected_foil_raw = self.foil_filter.currentText()
        selected_foil = "☆" if selected_foil_raw == "Foil" else "" if selected_foil_raw == "Non-foil" \
            else "Foil & Non-foil"
        selected_rarity = self.rarity_filter.currentText()
        selected_owned = self.owned_filter.currentText()

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 5)
            set_item = self.table.item(row, 1)
            variant_item = self.table.item(row, 3)
            foil_item = self.table.item(row, 4)
            rarity_item = self.table.item(row, 7)
            quantity_item = self.table.item(row, 11)

            name_matches = filter_text in name_item.text().lower()
            set_matches = (selected_set == "Alle Sets" or set_item.text() == selected_set)
            variant_matches = (selected_variant == "Alle Varianten" or variant_item.text() == selected_variant)
            foil_matches = (selected_foil == "Foil & Non-foil" or foil_item.text() == selected_foil)
            rarity_matches = (selected_rarity == "Alle Seltenheiten" or rarity_item.text() == selected_rarity)
            owned_matches = (selected_owned == "Alle Karten" or (
                        int(quantity_item.text()) > 0 and selected_owned == "Eigene Karten"))

            if name_matches and set_matches and variant_matches and foil_matches and rarity_matches and owned_matches:
                self.table.setRowHidden(row, False)
            else:
                self.table.setRowHidden(row, True)

    def show_data(self):
        cards = self.card_service.get_all_sw_cards()
        selected_user = self.user_filter.currentText()
        if not cards:
            print("No cards found!")
            return
        self.table.setRowCount(0)
        row_position = 0
        self.table.blockSignals(True)
        for card in cards:
            self.table.insertRow(row_position)
            item_id = QTableWidgetItem()
            item_id.setData(Qt.ItemDataRole.UserRole, card.id)
            self.table.setItem(row_position, 0, item_id)
            self.table.setItem(row_position, 1, QTableWidgetItem(card.set))
            self.table.setItem(row_position, 2, QTableWidgetItem(card.number))
            self.table.setItem(row_position, 3, QTableWidgetItem(card.variant))
            self.table.setItem(row_position, 4, QTableWidgetItem("☆" if card.foil else ""))
            self.table.setItem(row_position, 5, QTableWidgetItem(card.german_name))
            self.table.setItem(row_position, 6, QTableWidgetItem(card.german_subtitle))
            self.table.setItem(row_position, 7, QTableWidgetItem(card.rarity))
            self.table.setItem(row_position, 8, QTableWidgetItem(card.type))
            self.table.setItem(row_position, 9, QTableWidgetItem())
            link_label = QLabel()
            link_label.setText(f'<a href="{card.card_url}">Link</a>')
            link_label.setOpenExternalLinks(True)
            self.table.setCellWidget(row_position, 9, link_label)
            self.table.setItem(row_position, 10, QTableWidgetItem(
                str(self.price_service.get_latest_avg_7_price(card)) + "€"))
            user_id = self.user_service.get_user_id_by_name(selected_user)
            if user_id:
                quantity = self.user_service.get_quantity_of_card(user_id, card.id)
                self.table.setItem(row_position, 11, QTableWidgetItem(str(quantity)))
            else:
                self.table.setItem(row_position, 11, QTableWidgetItem(str(0)))
            btn_details = QPushButton('Details')
            btn_details.setProperty('id', card.id)
            btn_details.clicked.connect(self.show_details)
            self.table.setCellWidget(row_position, 12, btn_details)
            row_position += 1
        self.table.blockSignals(False)
        self.table.resizeColumnsToContents()
        value = self.card_service.get_value_of_owned_cards(selected_user)
        self.card_value.setText(f"Kartenwert: {value}€")

    def show_details(self):
        button = self.sender()
        card = self.card_service.get_sw_card_by_id(button.property('id'))
        dialog = CardDetailsDialog(card)
        dialog.exec()

    def add_card(self):
        dialog = InputDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            pass

    def add_user(self):
        dialog = AddUserDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            username = dialog.get_username()
            if username.strip():
                self.user_service.set_user(username)
                self.user_filter.addItem(username)


    def delete_data(self):
        pass

    def update_data(self, item):
        column = item.column()
        if column == 11:
            selected_user = self.user_filter.currentText()
            user_id = self.user_service.get_user_id_by_name(selected_user)
            new_quantity = item.text()
            id_item = self.table.item(item.row(), 0)
            id_value = id_item.data(Qt.ItemDataRole.UserRole)
            self.user_service.update_quantity_by_id(id_value, user_id, new_quantity)
            print(f"Updated id {id_value} with quantity: {new_quantity}")
            value = self.card_service.get_value_of_owned_cards(user_id)
            self.card_value.setText(f"Kartenwert: {value}€")


class CardDetailsDialog(QDialog):
    def __init__(self, card):
        super().__init__()
        self.setWindowTitle("Kartendetails")
        self.price_service = PriceService()
        layout = QVBoxLayout()

        # Add labels for card details
        layout.addWidget(QLabel(f"{card.german_name}"))
        layout.addWidget(QLabel(f"Untertitel: {card.german_subtitle}"))
        layout.addWidget(QLabel(f"Set: {card.set}"))
        layout.addWidget(QLabel(f"Nummer: {card.number}"))
        layout.addWidget(QLabel(f"Variante: {card.variant}"))
        layout.addWidget(QLabel(f"Foil: {'Ja' if card.foil else 'Nein'}"))
        layout.addWidget(QLabel(f"Seltenheit: {card.rarity}"))
        layout.addWidget(QLabel(f"ab: {self.price_service.get_lowest_price(card)}€"))
        layout.addWidget(QLabel(f"7-Tage Durchschnittspreis: {self.price_service.get_latest_avg_7_price(card)}€"))

        price_history = {price.date: float(price.price) for price in card.avg_7_days}
        dates = list(price_history.keys())
        prices = list(price_history.values())
        fig, ax = plt.subplots()
        ax.plot(dates, prices, marker='o', linestyle='-')
        ax.set_xlabel('Datum', color='white')
        ax.set_ylabel('Preis', color='white')
        ax.grid(True, linestyle='--')
        ax.set_facecolor('none')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        fig.patch.set_facecolor("None")
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['right'].set_color('white')
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color:'#222222';")
        layout.addWidget(canvas)

        self.setLayout(layout)


class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Input Dialog")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        self.inputs = {}
        fields = ["set", "number", "variant", "foil", "name", "subtitle", "rarity", "type", "card_url"]

        sets = ["SOR", "SOTG"]
        variants = ["Normal", "Hyperspace", "Showcase"]
        rarities = ["Common", "Uncommon", "Rare", "Legendary", "Special"]
        types = ["Unit", "Event", "Upgrade", "Leader", "Base"]

        for field in fields:
            if field == "set":
                combo_box = QComboBox(self)
                combo_box.addItems(sets)
                self.inputs[field] = combo_box
                form_layout.addRow(f"{field.capitalize()}:", combo_box)
            elif field == "variant":
                combo_box = QComboBox(self)
                combo_box.addItems(variants)
                self.inputs[field] = combo_box
                form_layout.addRow(f"{field.capitalize()}:", combo_box)
            elif field == "rarity":
                combo_box = QComboBox(self)
                combo_box.addItems(rarities)
                self.inputs[field] = combo_box
                form_layout.addRow(f"{field.capitalize()}:", combo_box)
            elif field == "type":
                combo_box = QComboBox(self)
                combo_box.addItems(types)
                self.inputs[field] = combo_box
                form_layout.addRow(f"{field.capitalize()}:", combo_box)
            elif field == "foil":
                checkbox = QCheckBox(self)
                self.inputs[field] = checkbox
                form_layout.addRow(f"{field.capitalize()}:", checkbox)
            else:
                line_edit = QLineEdit(self)
                self.inputs[field] = line_edit
                form_layout.addRow(f"{field.capitalize()}:", line_edit)

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit)
        layout.addLayout(form_layout)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit(self):
        data = [line_edit.text() for line_edit in self.inputs]
        print("Eingabedaten:", data)
        self.accept()


class AddUserDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benutzer hinzufügen")
        layout = QVBoxLayout()
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Benutzername eingeben")
        layout.addWidget(self.username_input)

        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Abbrechen", self)
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def get_username(self):
        return self.username_input.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec())
