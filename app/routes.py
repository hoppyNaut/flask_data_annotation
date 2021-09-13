from flask import render_template, redirect, flash, url_for, request, jsonify
from app.forms import LoginForm
from app import app, db
from app.pager import Pagination
from app.models import AddressInfo

#2个路由
@app.route('/')
#1个视图函数
def index():
	addressInfo_list = AddressInfo.query.all()
	print(len(addressInfo_list))
	address_list = []
	annotation_list = []
	for addressInfo in addressInfo_list:
		# print(addressInfo)
		address_list.append(addressInfo.address)
		annotation_list.append(addressInfo.annotations)

	pager_obj = Pagination(request.args.get("page", 1), len(address_list), request.path, request.args, per_page_count=10, max_pager_count=10, addressInfo_list=addressInfo_list, address_list=address_list, annotation_list=annotation_list)
	# print(request.args)
	index_list = address_list[pager_obj.start:pager_obj.end]
	html = pager_obj.page_html()
	html_address = pager_obj.page_html_address()
	return render_template("main.html", address_list=address_list, html_address=html_address, html=html)

@app.route('/edit_panel/<int:address_id>', methods=['get','post'])
def showpanel(address_id):
	addressInfo = AddressInfo.query.filter_by(id=address_id).first()
	annotationInfo = addressInfo.annotations
	annotation_list = annotationInfo.split(' ')
	print("len(addressInfo.address):", len(addressInfo.address))
	print("len(annotation_list):",len(annotation_list))

	# print('annotation_list:',annotation_list)

	page_html_list = []
	for i in range(len(addressInfo.address)):
		id = "tag_" + str(i)
		character_item = '<div class="layui-inline"><label class="layui-form-label" style="font-size:16px">%s</label>' \
						 '<div class="layui-input-inline">' \
						 '<select name=%s id=%s lay-verify="required" lay-search>' \
						 '<option value="">请选择</option>' \
						 '<optgroup label="非实体部分,如标点符号">' \
						 '<option value="O">O</option>' \
						 '</optgroup>' \
						 '<optgroup label="省级行政区,如:省、自治区、直辖市">' \
						 '<option value="B-prov">B-prov</option>' \
						 '<option value="I-prov">I-prov</option>' \
						 '<option value="E-prov">E-prov</option>' \
						 '</optgroup>' \
						 '<optgroup label="地级行政区划，地级市、地区、自治州等">' \
						 '<option value="B-city">B-city</option>' \
						 '<option value="I-city">I-city</option>' \
						 '<option value="E-city">E-city</option>' \
						 '</optgroup>' \
						 '<optgroup label="县级行政区划，市辖区、县级市、县等">' \
						 '<option value="B-district">B-district</option>' \
						 '<option value="I-district">I-district</option>' \
						 '<option value="E-district">E-district</option>' \
						 '</optgroup>' \
						 '<optgroup label="广义的上的开发区">' \
						 '<option value="B-devzone">B-devzone</option>' \
						 '<option value="I-devzone">I-devzone</option>' \
						 '<option value="E-devzone">E-devzone</option>' \
						 '</optgroup>' \
						 '<optgroup label="乡级行政区划，镇、街道、乡等">' \
						 '<option value="B-town">B-town</option>' \
						 '<option value="I-town">I-town</option>' \
						 '<option value="E-town">E-town</option>' \
						 '</optgroup>' \
						 '<optgroup label="社区、村等">' \
						 '<option value="B-community">B-community</option>' \
						 '<option value="I-community">I-community</option>' \
						 '<option value="E-community">E-community</option>' \
						 '</optgroup>' \
						 '<optgroup label="限定 xx 组、xx 队、xx 社（xx 为数字）">' \
						 '<option value="B-village_group">B-village_group</option>' \
						 '<option value="I-village_group">I-village_group</option>' \
						 '<option value="E-village_group">E-village_group</option>' \
						 '</optgroup>' \
						 '<optgroup label="有正式名称的道路，包括隧道、高架、街、弄、巷等">' \
						 '<option value="B-road">B-road</option>' \
						 '<option value="I-road">I-road</option>' \
						 '<option value="E-road">E-road</option>' \
						 '</optgroup>' \
						 '<optgroup label="路号">' \
						 '<option value="B-roadno">B-roadno</option>' \
						 '<option value="I-roadno">I-roadno</option>' \
						 '<option value="E-roadno">E-roadno</option>' \
						 '</optgroup>' \
						 '<optgroup label="兴趣点">' \
						 '<option value="B-poi">B-poi</option>' \
						 '<option value="I-poi">I-poi</option>' \
						 '<option value="E-poi">E-poi</option>' \
						 '</optgroup>' \
						 '<optgroup label="子兴趣点">' \
						 '<option value="B-subpoi">B-subpoi</option>' \
						 '<option value="I-subpoi">I-subpoi</option>' \
						 '<option value="E-subpoi">E-subpoi</option>' \
						 '</optgroup>' \
						 '<optgroup label="楼栋号">' \
						 '<option value="B-houseno">B-houseno</option>' \
						 '<option value="I-houseno">I-houseno</option>' \
						 '<option value="E-houseno">E-houseno</option>' \
						 '</optgroup>' \
						 '<optgroup label="单元号">' \
						 '<option value="B-cellno">B-cellno</option>' \
						 '<option value="I-cellno">I-cellno</option>' \
						 '<option value="E-cellno">E-cellno</option>' \
						 '</optgroup>' \
						 '<optgroup label="楼层号">' \
						 '<option value="B-floorno">B-floorno</option>' \
						 '<option value="I-floorno">I-floorno</option>' \
						 '<option value="E-floorno">E-floorno</option>' \
						 '</optgroup>' \
						 '<optgroup label="房间号、户号">' \
						 '<option value="B-roomno">B-roomno</option>' \
						 '<option value="I-roomno">I-roomno</option>' \
						 '<option value="E-roomno">E-roomno</option>' \
						 '</optgroup>' \
						 '<optgroup label="poi 内部的四层关系（house,cell,floor, room）没明确是哪一层">' \
						 '<option value="B-detail">B-detail</option>' \
						 '<option value="I-detail">I-detail</option>' \
						 '<option value="E-detail">E-detail</option>' \
						 '</optgroup>' \
						 '<optgroup label="普通辅助定位词">' \
						 '<option value="B-assist">B-assist</option>' \
						 '<option value="I-assist">I-assist</option>' \
						 '<option value="E-assist">E-assist</option>' \
						 '<option value="S-assist">S-assist</option>' \
						 '</optgroup>' \
						 '<optgroup label="距离辅助定位词">' \
						 '<option value="B-distance">B-distance</option>' \
						 '<option value="I-distance">I-distance</option>' \
						 '<option value="E-distance">E-distance</option>' \
						 '<option value="S-distance">S-distance</option>' \
						 '</optgroup>' \
						 '<optgroup label="道路口，口、交叉口、道路（高速）出入口，一定与 road 同时出现">' \
						 '<option value="B-intersection">B-intersection</option>' \
						 '<option value="I-intersection">I-intersection</option>' \
						 '<option value="E-intersection">E-intersection</option>' \
						 '<option value="S-intersection">S-intersection</option>' \
						 '</optgroup>' \
						 '<optgroup label="以上标签未覆盖的情况，或者无法判断的地址元素">' \
						 '<option value="B-others">B-others</option>' \
						 '<option value="I-others">I-others</option>' \
						 '<option value="E-others">E-others</option>' \
						 '<option value="S-others">S-others</option>' \
						 '</optgroup>' \
						 "</select><script type='text/javascript'>$('#%s').val('%s');</script></div></div>"\
						 % (addressInfo.address[i], id, id, id, annotation_list[i])
		page_html_list.append(character_item)

		confirm_button = '<button id="confirm_button" type="submit" lay-filter="layui-form" class="layui-btn layui-btn-primary" onclick="btn_confirm_click(%s,%s)">确认标注结果</button>' % (address_id, i+1)

	return render_template("panel.html", addressInfo=addressInfo, panel_address=''.join(page_html_list), confirm_button=confirm_button)

@app.route('/address_request',methods=['get','post'])
def getaddress():
	id = request.form.get('id')
	addressInfo = AddressInfo.query.filter_by(id=id).first()
	res = {'id':id, 'address':addressInfo.address, 'annotations':addressInfo.annotations,
		   'edit':addressInfo.edit, 'uncertain':addressInfo.uncertain, 'sentence_length':len(addressInfo.address)}
	print(res)
	# 转换为json对象
	return jsonify(res)

@app.route('/help_panel', methods=['get','post'])
def show_help_panel():
	return render_template("help.html")

@app.route('/edit_panel/address_update', methods=['get','post'])
def updateaddress():
	id = request.form.get('id')
	annotations = request.form.get("annotations")
	print("id:", id, "annotations:", annotations)
	addressInfo = AddressInfo.query.filter_by(id=id).first()
	addressInfo.annotations = annotations
	# addressInfo.edit = 1
	db.session.add(addressInfo)
	db.session.commit()
	res = {'id': id, 'address': addressInfo.address, 'annotations': addressInfo.annotations,
		   'edit': addressInfo.edit, 'uncertain': addressInfo.uncertain}
	return jsonify(res)

@app.route('/ensure_address', methods=['get','post'])
def ensure():
	id = request.form.get('id')
	addressInfo = AddressInfo.query.filter_by(id=id).first()
	addressInfo.uncertain = 0
	addressInfo.edit = 1
	db.session.add(addressInfo)
	db.session.commit()
	res = {'id': id, 'address': addressInfo.address, 'annotations': addressInfo.annotations,
		   'edit': addressInfo.edit, 'uncertain': addressInfo.uncertain}
	return jsonify(res)

@app.route('/unsure_address', methods=['get','post'])
def unsure():
	id = request.form.get('id')
	addressInfo = AddressInfo.query.filter_by(id=id).first()
	addressInfo.uncertain = 1
	db.session.add(addressInfo)
	db.session.commit()
	res = {'id': id, 'address': addressInfo.address, 'annotations': addressInfo.annotations,
		   'edit': addressInfo.edit, 'uncertain': addressInfo.uncertain}
	return jsonify(res)
