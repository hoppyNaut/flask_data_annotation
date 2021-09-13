from datetime import datetime
# 加密密码
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class AddressInfo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	address = db.Column(db.String(120), index=True)
	annotations = db.Column(db.String(120), index=True)
	edit = db.Column(db.Boolean(), index=True, default=False)
	uncertain = db.Column(db.Boolean(), index=True, default=False)

	def __repr__(self):
		return '<address {}\n annotations {}\n edit:{} uncetain:{}>'.format(self.address, self.annotations, self.edit, self.uncertain)

	# 将annotations字符串转化成数组
	def analyzeAnnotationsToArray(self):
		annotationArray = self.annotations.split(' ')
		return annotationArray

	def updateAnnotations(self, id, annotations):
		addressInfo = AddressInfo.query.filter_by(id=id).first()
		addressInfo.annotations = annotations
		db.session.add(addressInfo)
		db.session.commit()

