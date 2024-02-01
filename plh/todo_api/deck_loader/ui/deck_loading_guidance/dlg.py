################################################################################
## Form generated from reading UI file 'dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, QSize, Qt
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QSizePolicy,
    QSlider,
    QStackedWidget,
    QWidget,
)


class Ui_dlg:
    def setupUi(self, dlg):
        if not dlg.objectName():
            dlg.setObjectName("dlg")
        dlg.resize(1128, 794)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlg.sizePolicy().hasHeightForWidth())
        dlg.setSizePolicy(sizePolicy)
        dlg.setMinimumSize(QSize(0, 0))
        dlg.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.title = QLabel(dlg)
        self.title.setObjectName("title")
        self.title.setGeometry(QRect(20, 0, 371, 41))
        font = QFont()
        font.setFamilies(["Segoe UI"])
        font.setPointSize(17)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setLayoutDirection(Qt.LeftToRight)
        self.title.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
        self.deck_layout_info_header = QLabel(dlg)
        self.deck_layout_info_header.setObjectName("deck_layout_info_header")
        self.deck_layout_info_header.setGeometry(QRect(30, 40, 141, 41))
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        font1.setPointSize(13)
        font1.setBold(True)
        self.deck_layout_info_header.setFont(font1)
        self.deck_layout_info_header.setLayoutDirection(Qt.LeftToRight)
        self.deck_layout_info_header.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.deck_layout_info_bullets = QLabel(dlg)
        self.deck_layout_info_bullets.setObjectName("deck_layout_info_bullets")
        self.deck_layout_info_bullets.setGeometry(QRect(50, 80, 911, 61))
        font2 = QFont()
        font2.setFamilies(["Segoe UI"])
        font2.setPointSize(11)
        font2.setBold(True)
        self.deck_layout_info_bullets.setFont(font2)
        self.deck_layout_info_bullets.setLayoutDirection(Qt.LeftToRight)
        self.deck_layout_info_bullets.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.simple_deck_layout_image = QLabel(dlg)
        self.simple_deck_layout_image.setObjectName("simple_deck_layout_image")
        self.simple_deck_layout_image.setGeometry(QRect(20, 180, 1071, 371))
        self.simple_deck_layout_image.setPixmap(
            QPixmap(":/images/images/DeckLayout.png"),
        )
        self.simple_deck_layout_image.setScaledContents(True)
        self.simple_deck_layout_header = QLabel(dlg)
        self.simple_deck_layout_header.setObjectName("simple_deck_layout_header")
        self.simple_deck_layout_header.setGeometry(QRect(30, 160, 371, 21))
        self.simple_deck_layout_header.setFont(font1)
        self.simple_deck_layout_header.setLayoutDirection(Qt.LeftToRight)
        self.simple_deck_layout_header.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_info_header = QLabel(dlg)
        self.carrier_info_header.setObjectName("carrier_info_header")
        self.carrier_info_header.setGeometry(QRect(30, 550, 71, 41))
        self.carrier_info_header.setFont(font1)
        self.carrier_info_header.setLayoutDirection(Qt.LeftToRight)
        self.carrier_info_header.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_info_bullets = QLabel(dlg)
        self.carrier_info_bullets.setObjectName("carrier_info_bullets")
        self.carrier_info_bullets.setGeometry(QRect(50, 590, 371, 61))
        self.carrier_info_bullets.setFont(font2)
        self.carrier_info_bullets.setLayoutDirection(Qt.LeftToRight)
        self.carrier_info_bullets.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.labware_info_header = QLabel(dlg)
        self.labware_info_header.setObjectName("labware_info_header")
        self.labware_info_header.setGeometry(QRect(30, 670, 81, 41))
        self.labware_info_header.setFont(font1)
        self.labware_info_header.setLayoutDirection(Qt.LeftToRight)
        self.labware_info_header.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.labware_info_bullets = QLabel(dlg)
        self.labware_info_bullets.setObjectName("labware_info_bullets")
        self.labware_info_bullets.setGeometry(QRect(50, 710, 821, 61))
        self.labware_info_bullets.setFont(font2)
        self.labware_info_bullets.setLayoutDirection(Qt.LeftToRight)
        self.labware_info_bullets.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_stack = QStackedWidget(dlg)
        self.carrier_stack.setObjectName("carrier_stack")
        self.carrier_stack.setGeometry(QRect(710, 570, 181, 131))
        self.plate_carrier = QWidget()
        self.plate_carrier.setObjectName("plate_carrier")
        self.plate_carrier_image = QLabel(self.plate_carrier)
        self.plate_carrier_image.setObjectName("plate_carrier_image")
        self.plate_carrier_image.setGeometry(QRect(30, 20, 151, 111))
        self.plate_carrier_image.setPixmap(
            QPixmap(":/images/images/PLT_CAR_L5MD_A00.png"),
        )
        self.plate_carrier_image.setScaledContents(True)
        self.plate_carrier_label = QLabel(self.plate_carrier)
        self.plate_carrier_label.setObjectName("plate_carrier_label")
        self.plate_carrier_label.setGeometry(QRect(0, 10, 101, 41))
        self.plate_carrier_label.setFont(font2)
        self.plate_carrier_label.setLayoutDirection(Qt.LeftToRight)
        self.plate_carrier_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_stack.addWidget(self.plate_carrier)
        self.tube_carrier = QWidget()
        self.tube_carrier.setObjectName("tube_carrier")
        self.tube_carrier_image = QLabel(self.tube_carrier)
        self.tube_carrier_image.setObjectName("tube_carrier_image")
        self.tube_carrier_image.setGeometry(QRect(30, 20, 151, 111))
        font3 = QFont()
        font3.setPointSize(10)
        self.tube_carrier_image.setFont(font3)
        self.tube_carrier_image.setPixmap(
            QPixmap(":/images/images/SMP_CAR_32_EPIL_A00.png"),
        )
        self.tube_carrier_image.setScaledContents(True)
        self.tube_carrier_label = QLabel(self.tube_carrier)
        self.tube_carrier_label.setObjectName("tube_carrier_label")
        self.tube_carrier_label.setGeometry(QRect(0, 10, 101, 41))
        self.tube_carrier_label.setFont(font2)
        self.tube_carrier_label.setLayoutDirection(Qt.LeftToRight)
        self.tube_carrier_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_stack.addWidget(self.tube_carrier)
        self.tip_carrier = QWidget()
        self.tip_carrier.setObjectName("tip_carrier")
        self.tip_carrier_image = QLabel(self.tip_carrier)
        self.tip_carrier_image.setObjectName("tip_carrier_image")
        self.tip_carrier_image.setGeometry(QRect(30, 20, 151, 111))
        self.tip_carrier_image.setPixmap(QPixmap(":/images/images/tip_car_480_a00.png"))
        self.tip_carrier_image.setScaledContents(True)
        self.tip_carrier_label = QLabel(self.tip_carrier)
        self.tip_carrier_label.setObjectName("tip_carrier_label")
        self.tip_carrier_label.setGeometry(QRect(0, 10, 101, 41))
        self.tip_carrier_label.setFont(font2)
        self.tip_carrier_label.setLayoutDirection(Qt.LeftToRight)
        self.tip_carrier_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_stack.addWidget(self.tip_carrier)
        self.vacuum_carrier = QWidget()
        self.vacuum_carrier.setObjectName("vacuum_carrier")
        self.vacuum_carrier_image = QLabel(self.vacuum_carrier)
        self.vacuum_carrier_image.setObjectName("vacuum_carrier_image")
        self.vacuum_carrier_image.setGeometry(QRect(30, 30, 151, 101))
        self.vacuum_carrier_image.setFont(font3)
        self.vacuum_carrier_image.setPixmap(
            QPixmap(":/images/images/BVS_Shaker0_A00.png"),
        )
        self.vacuum_carrier_image.setScaledContents(True)
        self.vacuum_carrier_label = QLabel(self.vacuum_carrier)
        self.vacuum_carrier_label.setObjectName("vacuum_carrier_label")
        self.vacuum_carrier_label.setGeometry(QRect(0, 10, 111, 41))
        self.vacuum_carrier_label.setFont(font2)
        self.vacuum_carrier_label.setLayoutDirection(Qt.LeftToRight)
        self.vacuum_carrier_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.carrier_stack.addWidget(self.vacuum_carrier)
        self.carrier_slider = QSlider(dlg)
        self.carrier_slider.setObjectName("carrier_slider")
        self.carrier_slider.setGeometry(QRect(720, 710, 160, 16))
        self.carrier_slider.setMaximum(3)
        self.carrier_slider.setOrientation(Qt.Horizontal)
        self.labware_stack = QStackedWidget(dlg)
        self.labware_stack.setObjectName("labware_stack")
        self.labware_stack.setGeometry(QRect(900, 570, 181, 131))
        self.biorad_plate_200 = QWidget()
        self.biorad_plate_200.setObjectName("biorad_plate_200")
        self.biorad_plate_200_image = QLabel(self.biorad_plate_200)
        self.biorad_plate_200_image.setObjectName("biorad_plate_200_image")
        self.biorad_plate_200_image.setGeometry(QRect(50, 50, 131, 81))
        self.biorad_plate_200_image.setPixmap(
            QPixmap(":/images/images/PlateBiorad200uL96Well.jpg"),
        )
        self.biorad_plate_200_image.setScaledContents(True)
        self.biorad_plate_200_label = QLabel(self.biorad_plate_200)
        self.biorad_plate_200_label.setObjectName("biorad_plate_200_label")
        self.biorad_plate_200_label.setGeometry(QRect(0, 10, 181, 41))
        self.biorad_plate_200_label.setFont(font2)
        self.biorad_plate_200_label.setLayoutDirection(Qt.LeftToRight)
        self.biorad_plate_200_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.biorad_plate_200_label.setWordWrap(True)
        self.labware_stack.addWidget(self.biorad_plate_200)
        self.thermo_plate_400 = QWidget()
        self.thermo_plate_400.setObjectName("thermo_plate_400")
        self.thermo_plate_400_label = QLabel(self.thermo_plate_400)
        self.thermo_plate_400_label.setObjectName("thermo_plate_400_label")
        self.thermo_plate_400_label.setGeometry(QRect(0, 10, 181, 41))
        self.thermo_plate_400_label.setFont(font2)
        self.thermo_plate_400_label.setLayoutDirection(Qt.LeftToRight)
        self.thermo_plate_400_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.thermo_plate_400_label.setWordWrap(True)
        self.thermo_plate_400_image = QLabel(self.thermo_plate_400)
        self.thermo_plate_400_image.setObjectName("thermo_plate_400_image")
        self.thermo_plate_400_image.setGeometry(QRect(50, 50, 131, 81))
        self.thermo_plate_400_image.setPixmap(
            QPixmap(":/images/images/PlateThermo400uL96Well.jpg"),
        )
        self.thermo_plate_400_image.setScaledContents(True)
        self.labware_stack.addWidget(self.thermo_plate_400)
        self.thermo_plate_1200 = QWidget()
        self.thermo_plate_1200.setObjectName("thermo_plate_1200")
        self.thermo_plate_1200_image = QLabel(self.thermo_plate_1200)
        self.thermo_plate_1200_image.setObjectName("thermo_plate_1200_image")
        self.thermo_plate_1200_image.setGeometry(QRect(50, 50, 131, 81))
        self.thermo_plate_1200_image.setPixmap(
            QPixmap(":/images/images/PlateThermo1200uL96Well.jpg"),
        )
        self.thermo_plate_1200_image.setScaledContents(True)
        self.thermo_plate_1200_label = QLabel(self.thermo_plate_1200)
        self.thermo_plate_1200_label.setObjectName("thermo_plate_1200_label")
        self.thermo_plate_1200_label.setGeometry(QRect(0, 10, 181, 41))
        self.thermo_plate_1200_label.setFont(font2)
        self.thermo_plate_1200_label.setLayoutDirection(Qt.LeftToRight)
        self.thermo_plate_1200_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.thermo_plate_1200_label.setWordWrap(True)
        self.labware_stack.addWidget(self.thermo_plate_1200)
        self.corning_plate_2000 = QWidget()
        self.corning_plate_2000.setObjectName("corning_plate_2000")
        self.corning_plate_2000_image = QLabel(self.corning_plate_2000)
        self.corning_plate_2000_image.setObjectName("corning_plate_2000_image")
        self.corning_plate_2000_image.setGeometry(QRect(50, 50, 131, 81))
        self.corning_plate_2000_image.setPixmap(
            QPixmap(":/images/images/PlateCorning2000uL96Well.jpg"),
        )
        self.corning_plate_2000_image.setScaledContents(True)
        self.corning_plate_2000_label = QLabel(self.corning_plate_2000)
        self.corning_plate_2000_label.setObjectName("corning_plate_2000_label")
        self.corning_plate_2000_label.setGeometry(QRect(0, 10, 181, 41))
        self.corning_plate_2000_label.setFont(font2)
        self.corning_plate_2000_label.setLayoutDirection(Qt.LeftToRight)
        self.corning_plate_2000_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.corning_plate_2000_label.setWordWrap(True)
        self.labware_stack.addWidget(self.corning_plate_2000)
        self.fliptube_plate = QWidget()
        self.fliptube_plate.setObjectName("fliptube_plate")
        self.fliptube_plate_image = QLabel(self.fliptube_plate)
        self.fliptube_plate_image.setObjectName("fliptube_plate_image")
        self.fliptube_plate_image.setGeometry(QRect(50, 50, 131, 81))
        self.fliptube_plate_image.setPixmap(
            QPixmap(":/images/images/flitptube-Rackjpg.jpg"),
        )
        self.fliptube_plate_image.setScaledContents(True)
        self.fliptube_plate_label = QLabel(self.fliptube_plate)
        self.fliptube_plate_label.setObjectName("fliptube_plate_label")
        self.fliptube_plate_label.setGeometry(QRect(0, 10, 181, 41))
        self.fliptube_plate_label.setFont(font2)
        self.fliptube_plate_label.setLayoutDirection(Qt.LeftToRight)
        self.fliptube_plate_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.fliptube_plate_label.setWordWrap(True)
        self.labware_stack.addWidget(self.fliptube_plate)
        self.agilent_lid = QWidget()
        self.agilent_lid.setObjectName("agilent_lid")
        self.agilent_lid_image = QLabel(self.agilent_lid)
        self.agilent_lid_image.setObjectName("agilent_lid_image")
        self.agilent_lid_image.setGeometry(QRect(50, 50, 131, 81))
        self.agilent_lid_image.setPixmap(QPixmap(":/images/images/LidAgilentBlack.jpg"))
        self.agilent_lid_image.setScaledContents(True)
        self.agilent_lid_label = QLabel(self.agilent_lid)
        self.agilent_lid_label.setObjectName("agilent_lid_label")
        self.agilent_lid_label.setGeometry(QRect(0, 10, 181, 41))
        self.agilent_lid_label.setFont(font2)
        self.agilent_lid_label.setLayoutDirection(Qt.LeftToRight)
        self.agilent_lid_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.agilent_lid_label.setWordWrap(True)
        self.labware_stack.addWidget(self.agilent_lid)
        self.ftr_tips = QWidget()
        self.ftr_tips.setObjectName("ftr_tips")
        self.ftr_tips_image = QLabel(self.ftr_tips)
        self.ftr_tips_image.setObjectName("ftr_tips_image")
        self.ftr_tips_image.setGeometry(QRect(50, 40, 131, 91))
        self.ftr_tips_image.setPixmap(QPixmap(":/images/images/TipFTR1000uL.png"))
        self.ftr_tips_image.setScaledContents(True)
        self.ftr_tips_label = QLabel(self.ftr_tips)
        self.ftr_tips_label.setObjectName("ftr_tips_label")
        self.ftr_tips_label.setGeometry(QRect(0, 10, 181, 41))
        self.ftr_tips_label.setFont(font2)
        self.ftr_tips_label.setLayoutDirection(Qt.LeftToRight)
        self.ftr_tips_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.ftr_tips_label.setWordWrap(True)
        self.labware_stack.addWidget(self.ftr_tips)
        self.ntr_tips = QWidget()
        self.ntr_tips.setObjectName("ntr_tips")
        self.ntr_tips_image = QLabel(self.ntr_tips)
        self.ntr_tips_image.setObjectName("ntr_tips_image")
        self.ntr_tips_image.setGeometry(QRect(50, 40, 131, 91))
        self.ntr_tips_image.setPixmap(QPixmap(":/images/images/TipNTR300uL.png"))
        self.ntr_tips_image.setScaledContents(True)
        self.ntr_tips_label = QLabel(self.ntr_tips)
        self.ntr_tips_label.setObjectName("ntr_tips_label")
        self.ntr_tips_label.setGeometry(QRect(0, 10, 181, 41))
        self.ntr_tips_label.setFont(font2)
        self.ntr_tips_label.setLayoutDirection(Qt.LeftToRight)
        self.ntr_tips_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.ntr_tips_label.setWordWrap(True)
        self.labware_stack.addWidget(self.ntr_tips)
        self.imcs_tips = QWidget()
        self.imcs_tips.setObjectName("imcs_tips")
        self.imcs_tips_image = QLabel(self.imcs_tips)
        self.imcs_tips_image.setObjectName("imcs_tips_image")
        self.imcs_tips_image.setGeometry(QRect(50, 50, 131, 81))
        self.imcs_tips_image.setPixmap(QPixmap(":/images/images/TipIMCSSizeX100.jpg"))
        self.imcs_tips_image.setScaledContents(True)
        self.imcs_tips_label = QLabel(self.imcs_tips)
        self.imcs_tips_label.setObjectName("imcs_tips_label")
        self.imcs_tips_label.setGeometry(QRect(0, 10, 181, 41))
        self.imcs_tips_label.setFont(font2)
        self.imcs_tips_label.setLayoutDirection(Qt.LeftToRight)
        self.imcs_tips_label.setAlignment(
            Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter,
        )
        self.imcs_tips_label.setWordWrap(True)
        self.labware_stack.addWidget(self.imcs_tips)
        self.labware_slider = QSlider(dlg)
        self.labware_slider.setObjectName("labware_slider")
        self.labware_slider.setGeometry(QRect(910, 710, 160, 16))
        self.labware_slider.setMaximum(8)
        self.labware_slider.setOrientation(Qt.Horizontal)
        self.carrier_info_header_2 = QLabel(dlg)
        self.carrier_info_header_2.setObjectName("carrier_info_header_2")
        self.carrier_info_header_2.setGeometry(QRect(730, 550, 151, 41))
        self.carrier_info_header_2.setFont(font1)
        self.carrier_info_header_2.setLayoutDirection(Qt.LeftToRight)
        self.carrier_info_header_2.setAlignment(Qt.AlignCenter)
        self.carrier_info_header_3 = QLabel(dlg)
        self.carrier_info_header_3.setObjectName("carrier_info_header_3")
        self.carrier_info_header_3.setGeometry(QRect(910, 550, 151, 41))
        self.carrier_info_header_3.setFont(font1)
        self.carrier_info_header_3.setLayoutDirection(Qt.LeftToRight)
        self.carrier_info_header_3.setAlignment(Qt.AlignCenter)
        self.thank_you_button = QPushButton(dlg)
        self.thank_you_button.setObjectName("thank_you_button")
        self.thank_you_button.setGeometry(QRect(900, 740, 181, 41))
        font4 = QFont()
        font4.setPointSize(14)
        font4.setBold(True)
        self.thank_you_button.setFont(font4)
        self.thank_you_button.setStyleSheet("background: #39FF14")
        QWidget.setTabOrder(self.carrier_slider, self.labware_slider)

        self.retranslateUi(dlg)
        self.carrier_slider.valueChanged.connect(self.carrier_stack.setCurrentIndex)
        self.labware_slider.valueChanged.connect(self.labware_stack.setCurrentIndex)

        self.carrier_stack.setCurrentIndex(0)
        self.labware_stack.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(dlg)

    # setupUi

    def retranslateUi(self, dlg):
        dlg.setWindowTitle(
            QCoreApplication.translate("dlg", "Deck Loading Guidance", None),
        )
        self.title.setText(
            QCoreApplication.translate("dlg", "Hamilton Deck Loading Guidance", None),
        )
        self.deck_layout_info_header.setText(
            QCoreApplication.translate("dlg", "Deck Layout:", None),
        )
        self.deck_layout_info_bullets.setText(
            QCoreApplication.translate(
                "dlg",
                "1. A deck layout contains all the possible labware positions (as X, Y, Z coordinates) supported by your instrument.\n"
                "2. Layouts conviently organize labware onto carriers.\n"
                "3. To properly load a deck, you should satisfy all the required labware positions by loading the correct carrier and carrier positions.",
                None,
            ),
        )
        self.simple_deck_layout_image.setText("")
        self.simple_deck_layout_header.setText(
            QCoreApplication.translate(
                "dlg",
                "Below is an example of a simple deck layout:",
                None,
            ),
        )
        self.carrier_info_header.setText(
            QCoreApplication.translate("dlg", "Carriers:", None),
        )
        self.carrier_info_bullets.setText(
            QCoreApplication.translate(
                "dlg",
                "Carriers organize labware along the Y axis.\n"
                "Carriers support different types of labware\n"
                "Examples of different carriers are shown to the right.",
                None,
            ),
        )
        self.labware_info_header.setText(
            QCoreApplication.translate("dlg", "Labware:", None),
        )
        self.labware_info_bullets.setText(
            QCoreApplication.translate(
                "dlg",
                "Labware is a specific definition of a plate, which includes number of wells and well geometry\n"
                "You can NOT substitute labware. The Hamilton expects a specific labware and will crash if the wrong labware is used.\n"
                "Examples of labware are Tips, Plates, Lids, Heaters, Vacuums, and Tubes.",
                None,
            ),
        )
        self.plate_carrier_image.setText("")
        self.plate_carrier_label.setText(
            QCoreApplication.translate("dlg", "Plate Carrier", None),
        )
        self.tube_carrier_image.setText("")
        self.tube_carrier_label.setText(
            QCoreApplication.translate("dlg", "Tube Carrier", None),
        )
        self.tip_carrier_image.setText("")
        self.tip_carrier_label.setText(
            QCoreApplication.translate("dlg", "Tip Carrier", None),
        )
        self.vacuum_carrier_image.setText("")
        self.vacuum_carrier_label.setText(
            QCoreApplication.translate("dlg", "Vacuum Carrier", None),
        )
        self.biorad_plate_200_image.setText("")
        self.biorad_plate_200_label.setText(
            QCoreApplication.translate("dlg", "Biorad 200uL Plate", None),
        )
        self.thermo_plate_400_label.setText(
            QCoreApplication.translate("dlg", "Thermo 400uL Plate", None),
        )
        self.thermo_plate_400_image.setText("")
        self.thermo_plate_1200_image.setText("")
        self.thermo_plate_1200_label.setText(
            QCoreApplication.translate("dlg", "Thermo 1200uL Plate", None),
        )
        self.corning_plate_2000_image.setText("")
        self.corning_plate_2000_label.setText(
            QCoreApplication.translate("dlg", "Corning 2000uL Plate", None),
        )
        self.fliptube_plate_image.setText("")
        self.fliptube_plate_label.setText(
            QCoreApplication.translate("dlg", "Hamilton FlipTube Plate", None),
        )
        self.agilent_lid_image.setText("")
        self.agilent_lid_label.setText(
            QCoreApplication.translate("dlg", "Agilent Black Lid", None),
        )
        self.ftr_tips_image.setText("")
        self.ftr_tips_label.setText(
            QCoreApplication.translate("dlg", "Filtered Tip Rack (FTR)", None),
        )
        self.ntr_tips_image.setText("")
        self.ntr_tips_label.setText(
            QCoreApplication.translate("dlg", "Nested Tip Rack (NTR)", None),
        )
        self.imcs_tips_image.setText("")
        self.imcs_tips_label.setText(
            QCoreApplication.translate("dlg", "IMCS Desalting Tips", None),
        )
        self.carrier_info_header_2.setText(
            QCoreApplication.translate("dlg", "Carrier Examples", None),
        )
        self.carrier_info_header_3.setText(
            QCoreApplication.translate("dlg", "Labware Examples", None),
        )
        self.thank_you_button.setText(
            QCoreApplication.translate("dlg", "Thank You!", None),
        )

    # retranslateUi
