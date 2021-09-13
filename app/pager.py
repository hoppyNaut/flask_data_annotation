import string
from urllib.parse import urlencode,quote,unquote
from app.models import AddressInfo

class Pagination(object):
    """
    自定义分页
    """
    def __init__(self,current_page,total_count,base_url,params,per_page_count=100,max_pager_count=11, addressInfo_list=[], address_list=[], annotation_list=[]):
        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        if current_page <=0:
            current_page = 1
        self.current_page = current_page

        self.address_list = address_list
        self.annotation_list = annotation_list
        self.addressInfo_list = addressInfo_list
        # 数据总条数
        self.total_count = total_count

        # 每页显示10条数据
        self.per_page_count = per_page_count

        # 页面上应该显示的最大页码
        max_page_num, div = divmod(total_count, per_page_count)
        if div:
            max_page_num += 1
        self.max_page_num = max_page_num

        # 页面上默认显示11个页码（当前页在中间）
        self.max_pager_count = max_pager_count
        self.half_max_pager_count = int((max_pager_count - 1) / 2)

        # URL前缀
        self.base_url = base_url

        # request.GET
        import copy
        params = copy.deepcopy(params)
        # params._mutable = True
        get_dict = params.to_dict()
        # 包含当前列表页面所有的搜/索条件
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # self.params[page] = 8
        # self.params.urlencode()
        # source=2&status=2&gender=2&consultant=1&page=8
        # href="/hosts/?source=2&status=2&gender=2&consultant=1&page=8"
        # href="%s?%s" %(self.base_url,self.params.urlencode())
        self.params = get_dict

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    def page_html_address(self):
        page_html_list = []
        for i in range(self.per_page_count * (self.current_page - 1) + 1, min(self.per_page_count * self.current_page + 1, len(self.addressInfo_list) + 1)):
            uncertain = self.addressInfo_list[i - 1].uncertain
            edit = self.addressInfo_list[i - 1].edit
            id = "address_id_" + str(i)
            if uncertain == True:
                address_item = '<li class="list-group-item" style="background-color:#FFDAB9"><span id=%s>%s</span>' \
                               '<h4>地址信息：%s</h4><h4>标注信息：%s' \
                               '</h4><div class="btn-group" role="group" aria-label="...">' \
                               '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_edit_click(%s)">编辑</button>' \
                               '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_unsure_click(%s)">不确定</button>' \
                               '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_ensure_click(%s)">确定</button></div></li>' \
                               %  (id, i, self.address_list[i - 1], self.annotation_list[i - 1], i, i, i)
            else:
                if edit == True:
                    address_item = '<li class="list-group-item" style="background-color:#cde6c7"><span id=%s>%s</span>' \
                                   '<h4>地址信息：%s</h4><h4>标注信息：%s' \
                                   '</h4><div class="btn-group" role="group" aria-label="...">' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_edit_click(%s)">编辑</button>' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_unsure_click(%s)">不确定</button>' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_ensure_click(%s)">确定</button></div></li>'\
                                    % (id, i, self.address_list[i - 1], self.annotation_list[i - 1], i, i, i)
                else:
                    address_item = '<li class="list-group-item"><span id=%s>%s</span>' \
                                   '<h4>地址信息：%s</h4><h4>标注信息：%s' \
                                   '</h4><div class="btn-group" role="group" aria-label="...">' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_edit_click(%s)">编辑</button>' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_unsure_click(%s)">不确定</button>' \
                                   '<button class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" onclick="btn_ensure_click(%s)">确定</button></div></li>' \
                                   % (id, i, self.address_list[i - 1], self.annotation_list[i - 1], i, i, i)

            page_html_list.append(address_item)

        return ''.join(page_html_list)

    def page_html(self):
        # 如果总页数 <= 11
        if self.max_page_num <= self.max_pager_count:
            pager_start = 1
            pager_end = self.max_page_num
        # 如果总页数 > 11
        else:
            # 如果当前页 <= 5
            if self.current_page <= self.half_max_pager_count:
                pager_start = 1
                pager_end = self.max_pager_count
            else:
                # 当前页 + 5 > 总页码
                if (self.current_page + self.half_max_pager_count) > self.max_page_num:
                    pager_end = self.max_page_num
                    pager_start = self.max_page_num - self.max_pager_count + 1   #倒这数11个
                else:
                    pager_start = self.current_page - self.half_max_pager_count
                    pager_end = self.current_page + self.half_max_pager_count

        page_html_list = []
        # {source:[2,], status:[2], gender:[2],consultant:[1],page:[1]}
        # 首页
        self.params['page'] = 1
        first_page = '<li><a href="%s?%s">首页</a></li>' % (self.base_url,urlencode(self.params),)
        page_html_list.append(first_page)
        # 上一页
        self.params["page"] = self.current_page - 1
        if self.params["page"] < 1:
            pervious_page = '<li class="disabled"><a href="%s?%s" aria-label="Previous">上一页</span></a></li>' % (self.base_url, urlencode(self.params))
        else:
            pervious_page = '<li><a href = "%s?%s" aria-label = "Previous" >上一页</span></a></li>' % ( self.base_url, urlencode(self.params))
        page_html_list.append(pervious_page)
        # 中间页码
        for i in range(pager_start, pager_end + 1):
            self.params['page'] = i
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?%s">%s</a></li>' % (self.base_url,urlencode(self.params), i,)
            else:
                temp = '<li><a href="%s?%s">%s</a></li>' % (self.base_url,urlencode(self.params), i,)
            page_html_list.append(temp)

        # 下一页
        self.params["page"] = self.current_page + 1
        if self.params["page"] > self.max_page_num:
            self.params["page"] = self.current_page
            next_page = '<li class="disabled"><a href = "%s?%s" aria-label = "Next">下一页</span></a></li >' % (self.base_url, urlencode(self.params))
        else:
            next_page = '<li><a href = "%s?%s" aria-label = "Next">下一页</span></a></li>' % (self.base_url, urlencode(self.params))
        page_html_list.append(next_page)

        # 尾页
        self.params['page'] = self.max_page_num
        last_page = '<li><a href="%s?%s">尾页</a></li>' % (self.base_url, urlencode(self.params),)
        page_html_list.append(last_page)

        # 跳转
        # input_page = '<form class="form-inline">'\
        #                     '<div class="form-group">'\
        #                         '<input id="page_input" type="text" min="1" max="2000" class="form-control" placeholder="请输入跳转页面(1~1000)" oninput="change_href()" onkeydown="keyup_submit(event);">'\
        #                         '<a role="button" href="%s?page=%s" id="page_jump" class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm">跳转</a>'\
        #                     '</div>'\
        #                 '</form>' % (self.base_url,self.current_page)

        input_page = '<input id="page_input" type="text" min="1" max="2000" style="width:40px; margin-left:5px" placeholder="请输入跳转页面(1~2003)" oninput="change_href()" onkeydown="keyup_submit(event);">' \
                     '<a role="button" href="%s?page=%s" id="page_jump" class="layui-btn layui-btn-primary layui-border-blue layui-btn-sm" style="margin-left:5px">跳转</a>' \
                    % (self.base_url, self.current_page)
        page_html_list.append(input_page)

        return ''.join(page_html_list)