from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
import sys
import os
import os.path
import configparser
import json
import requests
import logger
from jadepy import JadeAPI

NETWORK = 'testnet'

class AppWindow():
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        bundle_dir = getattr(
            sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        path_to_dialog_ui = os.path.abspath(
            os.path.join(bundle_dir, 'dialog.ui'))
        self.ui = loader.load(path_to_dialog_ui, None)

        self.ui.btn_connect.clicked.connect(self.on_btn_connect_clicked_send)
        self.ui.btn_xpub.clicked.connect(self.on_btn_xpub_clicked_send)
        self.ui.btn_address.clicked.connect(self.on_btn_address_clicked_send)
        self.ui.btn_sign.clicked.connect(self.on_btn_sign_clicked_send)

    def on_btn_connect_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=120) as jade:
            version_info = jade.get_version_info()
            while jade.auth_user(NETWORK) is not True:
                print('Error - please try again')

            self.ui.txt_info_version.setText(version_info.get('JADE_VERSION', ''))
            self.ui.txt_info_otamaxchunk.setText(str(version_info.get('JADE_OTA_MAX_CHUNK', '')))
            self.ui.txt_info_config.setText(version_info.get('JADE_CONFIG', ''))
            self.ui.txt_info_board.setText(version_info.get('BOARD_TYPE', ''))
            self.ui.txt_info_features.setText(version_info.get('JADE_FEATURES', ''))
            self.ui.txt_info_idfversion.setText(version_info.get('IDF_VERSION', ''))
            self.ui.txt_info_chip.setText(version_info.get('CHIP_FEATURES', ''))
            self.ui.txt_info_efusemac.setText(version_info.get('EFUSEMAC', ''))
            self.ui.txt_info_battery.setText(str(version_info.get('BATTERY_STATUS', '')))
            self.ui.txt_info_state.setText(version_info.get('JADE_STATE', ''))
            self.ui.txt_info_networks.setText(version_info.get('JADE_NETWORKS', ''))
            self.ui.txt_info_haspin.setText(str(version_info.get('JADE_HAS_PIN', '')))
            # enable guis objects
            self.ui.btn_connect.setEnabled(False);
            self.ui.grp_info.setEnabled(True);
            self.ui.grp_sign.setEnabled(True);
            # debug
            self.ui.txt_results.setText(json.dumps(version_info) + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_xpub_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=120) as jade:
            while jade.auth_user(NETWORK) is not True:
                print('Error - please try again')
            xpub = jade.get_xpub(NETWORK, [0x80000000+44, 0x80000000+1, 0x80000000])
            self.ui.txt_xpub.setText(xpub)
            # debug
            self.ui.txt_results.setText(xpub + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_address_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=120) as jade:
            while jade.auth_user(NETWORK) is not True:
                print('Error - please try again')
            address = jade.get_receive_address(NETWORK, [0x80000000+44, 0x80000000+1, 0x80000000, 0, 0], variant='pkh(k)')
            self.ui.txt_address.setText(address)
            # debug
            self.ui.txt_results.setText(address + '\n' + self.ui.txt_results.toPlainText())

    def on_btn_sign_clicked_send(self):
        with JadeAPI.create_serial(device=self.ui.txt_port.text(), timeout=120) as jade:
            while jade.auth_user(NETWORK) is not True:
                print('Error - please try again')
            signature = jade.sign_message([0x80000000+44, 0x80000000+1, 0x80000000, 0, 0],  self.ui.txt_message.text())
            self.ui.txt_signature.setText(signature)
            # debug
            self.ui.txt_results.setText(signature + '\n' + self.ui.txt_results.toPlainText())


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = AppWindow()
    w.ui.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = AppWindow()
    w.ui.show()
    sys.exit(app.exec_())
