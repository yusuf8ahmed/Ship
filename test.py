import qrcode

qr = qrcode.QRCode()
qr.add_data("http://192.168.2.178:9000")
im = qr.make_image()
im.show()