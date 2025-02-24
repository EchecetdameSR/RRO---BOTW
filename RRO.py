import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QTabWidget, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

class RupeeRouteOptimizer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("RRO - All Dungeons [BL] 💎")
        self.setWindowIcon(QIcon.fromTheme("dollar"))
        self.setFixedSize(500, 400)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        # Mode sombre
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFF;
                font-family: Arial, sans-serif;
            }
            QLabel {
                font-size: 14px;
                color: #FFF;
            }
            QPushButton {
                background-color: #444;
                color: #FFF;
                border: 1px solid #555;
                padding: 6px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #666;
            }
            QLineEdit {
                background-color: #444;
                border: 1px solid #555;
                padding: 6px;
                font-size: 14px;
                color: #FFF;
            }
            QTabWidget::pane {
                border: 1px solid #555;
            }
            QTabWidget::tab-bar {
                alignment: center;
            }
            QTabWidget::tab {
                background: #444;
                border: 1px solid #555;
                color: #000000;
                padding: 8px;
                min-width: 100px;
            }
            QTabWidget::tab:selected {
                color: #000;  # Texte noir pour l'onglet sélectionné
                font-weight: bold;
                background-color: #444;
            }
            QTabWidget::tab:hover {
                background: #000000;
            }
            QTabWidget::tab {
                color: #000;  /* Change le texte des onglets en noir */
            }

        """)
        

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "🧑‍💻 First Part")
        self.tabs.addTab(self.tab2, "📊 Second Part")

        self.initTab1()
        self.initTab2()

        layout = QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def initTab1(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Label header
        header_label = QLabel("💰 Rupee Route Optimizer 💰")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header_label)

        self.stones = {"Ruby": 210, "Diamond": 500, "Topaz": 180, "Sapphire": 270}
        self.counts = {stone: 0 for stone in self.stones}
        self.labels = {}

        for stone, value in self.stones.items():
            hbox = QHBoxLayout()
            label = QLabel(f"{stone}: 0 {self.getStoneEmoji(stone)}")
            self.labels[stone] = label
            btn_minus = QPushButton("➖")
            btn_plus = QPushButton("➕")

            btn_minus.setStyleSheet("background-color: #555; border: 1px solid #666; padding: 5px;")
            btn_plus.setStyleSheet("background-color: #555; border: 1px solid #666; padding: 5px;")

            btn_minus.clicked.connect(lambda _, s=stone: self.updateCount(s, -1))
            btn_plus.clicked.connect(lambda _, s=stone: self.updateCount(s, 1))

            hbox.addWidget(btn_minus)
            hbox.addWidget(label)
            hbox.addWidget(btn_plus)
            layout.addLayout(hbox)

        self.total_label = QLabel("Total Rupees: 210 💰")
        self.total_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_label)

        self.backup_label = QLabel("Backup Needed: None ❌")
        self.backup_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.backup_label)

        self.tab1.setLayout(layout)
        self.updateTotal()

    def getStoneEmoji(self, stone):
        emojis = {
            "Ruby": "🔻",
            "Diamond": "💎",
            "Topaz": "🟨",
            "Sapphire": "🔷"
        }
        return emojis.get(stone, "💎")

    def updateCount(self, stone, delta):
        self.counts[stone] = max(0, self.counts[stone] + delta)
        self.labels[stone].setText(f"{stone}: {self.counts[stone]} {self.getStoneEmoji(stone)}")
        self.updateTotal()

    def updateTotal(self):
        total = 210 + sum(self.counts[s] * v for s, v in self.stones.items())
        self.total_label.setText(f"Total Rupees: {total} 💰")

        if total >= 684:
            self.backup_label.setText("Backup Needed: None ❌")
        elif total + 270 >= 684:
            self.backup_label.setText("Backup Needed: Medoh Chest (Sapphire) 🔷")
        elif total + 370 >= 684:
            self.backup_label.setText("Backup Needed: Medoh Chest + Bazaar 100 💵")
        else:
            self.backup_label.setText("Impossible to continue the run quickly 🚫")

    def initTab2(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Label header
        layout.addWidget(QLabel("Enter Rupees at Riju's Cutscene :"), alignment=Qt.AlignLeft)

        # Input field
        self.riju_input = QLineEdit()
        self.riju_input.setPlaceholderText("Enter your current Rupees 💰...")
        self.riju_input.setAlignment(Qt.AlignCenter)
        self.riju_input.setStyleSheet("background-color: #555; border: 1px solid #666; padding: 5px;")
        self.riju_input.textChanged.connect(self.calculateOptimalRoute)
        layout.addWidget(self.riju_input)

        # Route output
        self.route_label = QLabel("Best route: Waiting for input... 🕒")
        self.route_label.setAlignment(Qt.AlignLeft)
        self.route_label.setWordWrap(True)
        layout.addWidget(self.route_label)

        # Total after route
        self.total_after_route_label = QLabel("Total after route: 0 💰")
        self.total_after_route_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.total_after_route_label)

        self.tab2.setLayout(layout)

    def calculateOptimalRoute(self):
        try:
            current_rup = int(self.riju_input.text())
        except ValueError:
            self.route_label.setText("Invalid input ❌")
            self.total_after_route_label.setText("Total after route: 0 💰")
            return

        needed = max(0, 1160 - current_rup)
        route = []
        loot = [("Topaz", 180), ("100 Rupees Chest", 100), ("Topaz Chest 1", 180), ("Topaz Chest 2", 180), ("Ruby Chest", 210), ("600 Rupees Chest", 600)]

        total_route = current_rup
        for item, value in loot:
            if needed <= 0:
                break
            route.append(f"Take {item} (+{value} 💰)")
            total_route += value
            needed -= value

        if needed > 0:
            self.route_label.setText("Not enough rupees available 🚫")
            self.total_after_route_label.setText(f"Total after route: {total_route} 💰")
        else:
            self.route_label.setText("Best route:\n" + "\n".join(route))
            self.total_after_route_label.setText(f"Total after route: {total_route} 💰")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RupeeRouteOptimizer()
    window.show()
    sys.exit(app.exec_())
