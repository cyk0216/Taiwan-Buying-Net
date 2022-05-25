# main.py
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, text, desc
from flask import Flask
from flask import render_template
from flask import request
# from flask_migrate import Migrate
import os
import time

# from flask import request, redirect, url_for, time

# db = SQLAlchemy()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
# 初始化Flask物件，並貼上app這個標籤。

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 減少記憶體使用
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tbnc_admin:ixTech0924_@54.95.212.201:3306/BiddingNet_Backup"

# "mysql+pymysql://kaitester:ix321987@localhost:3307/biddingnet"
# "mysql+pymysql://tbnc_admin:ixTech0924_@54.95.212.201:3306/BiddingNet"
# "mysql+pymysql://tbnc_admin:ixTech0924_@54.95.212.201:3306/BiddingNet_Backup"

db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# 新增資料庫欄位用

# mysql db setting
# user_name:password@host_name:port/db_name
# ROWS_PER_PAGE = 6

# 模型定義(model)


class company_table(db.Model):
    # CREATE TABLE Company_table(
    __table__name = 'company_table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    Company_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # -> Company_id int NOT NULL,
    Company_Name = db.Column(db.String(80), nullable=False)
    # -> Company_Name nvarchar(50) NULL
    Company_Type_id = db.Column(db.Integer, db.ForeignKey('type_table.Type_id'), nullable=False, default=1)
    # -> Company_Type_id int NOT NULL, FK1(=type_table('Type_id'))

    db_Company_User = db.relationship("user_table", backref="company_table")
    # ->Company_table = user_table 關聯性(一對多PK1)
    db_Company_Bidder = db.relationship("bidder_table", backref="company_table")
    # ->company_table = bidder_table 關聯性(一對多PK2)
    db_Company_Case = db.relationship("case_table", backref="company_table")
    # ->Case_table = company_table 關聯性(一對多PK3)

    def __init__(self, Company_id, Company_Name, Company_Type_id):
        self.Company_id = Company_id
        self.Company_Name = Company_Name
        self.Company_Type_id = Company_Type_id


class user_table(db.Model):
    # CREATE TABLE User_table(
    __table__name = 'user_table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    User_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # -> User_id int NOT NULL,
    User_ref_id = db.Column(db.String(80), nullable=False)
    # -> User_ref_id nvarchar(50) NULL,
    User_Name = db.Column(db.String(80), nullable=False)
    # -> User_Name nvarchar(50) NULL,
    User_Email = db.Column(db.String(80), nullable=False)
    # -> User_Email nvarchar(50) NULL,
    User_Password = db.Column(db.String(80), nullable=False, unique=True)
    # -> User_Password nvarchar(50) NULL,
    User_Favorite_Company_id = db.Column(db.Integer, db.ForeignKey('company_table.Company_id'))
    # -> User_Favorite_Company_id int NULL, FK1(=Company_table('Company_id'))
    User_Favorite_Case_id = db.Column(db.Integer, db.ForeignKey('case_table.Case_id'))
    # -> User_Favorite_Case_Name int NULL, FK2(=Case_table('Case_id'))

    def __init__(
        self, User_id, User_ref_id, User_Name, User_Email, User_Password,
            User_Favorite_Company, User_Favorite_Case_Name
    ):
        self.User_id = User_id
        self.User_ref_id = User_ref_id
        self.User_Name = User_Name
        self.User_Email = User_Email
        self.User_Password = User_Password
        self.User_Favorite_Company = User_Favorite_Company
        self.User_Favorite_Case_Name = User_Favorite_Case_Name


class bidder_table(db.Model):
    # CREATE TABLE Bidder_table(
    __table__name = 'bidder_Table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    Bidder_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # -> Bidder_id int NOT NULL,
    Bidder_case_id = db.Column(db.Integer, db.ForeignKey('case_table.Case_id'), nullable=False)
    # -> Bidder_Case_id int NOT NULL,, FK1(=Case_table('Case_id')
    Bidder_company_id = db.Column(db.Integer, db.ForeignKey('company_table.Company_id'), nullable=False)
    # -> Bidder_Company_id int NOT NULL, FK2(=Company_table('Company_id'))
    Bidder_case_price = db.Column(db.Integer)
    # -> Bidder_Case_Price int NULL
    Bidder_get_case = db.Column(db.Boolean, nullable=False)
    # -> Bidder_Get_Case bit NOT NULL

    def __init__(
        self, Bidder_id, Bidder_case_id, Bidder_company_id,
            Bidder_case_price, Bidder_get_case
    ):
        self.Bidder_id = Bidder_id
        self.Bidder_case_id = Bidder_case_id
        self.Bidder_company_id = Bidder_company_id
        self.Bidder_case_price = Bidder_case_price
        self.Bidder_get_case = Bidder_get_case


class case_table(db.Model):
    # CREATE TABLE Case_Table(
    __table__name = 'case_table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    Case_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # -> Case_id int NOT NULL,
    Case_ref_id = db.Column(db.Integer, unique=True, nullable=False)
    # -> Case_ref_id int NOT NULL,
    Case_Name = db.Column(db.String(100), nullable=False)
    # -> Case_Name nvarchar(50) NOT NULL,
    Case_Tender_Unit_id = db.Column(db.Integer, db.ForeignKey('tender_unit_table.Tender_Unit_id'), nullable=False)
    # -> Case_Tender_Unit nvarchar(50) NOT NULL,
    #    FK1(=Tender_Unit_table('Tender_Unit_id'))
    Case_Company_id = db.Column(db.Integer, db.ForeignKey('company_table.Company_id'))
    # -> Case_Company nvarchar(50) NOT NULL,
    #    FK2(=Company_table('Company_id'))
    Case_Budget_Price = db.Column(db.Integer)
    # -> Case_Budget_Price int NULL,
    Case_Final_Price = db.Column(db.Integer)
    # -> Case_Final_Price int NULL,
    Case_Start_Date = db.Column(db.DateTime)
    # -> Case_Start_Date date NULL,
    Case_End_Date = db.Column(db.DateTime)
    # -> Case_End_Date date NULL,
    Case_be_gotten = db.Column(db.Boolean, nullable=False)
    # -> Case_be_gotten bit NULL

    db_Case_User = db.relationship("user_table", backref="case_table")
    # ->Case_table = User_table 關聯性(一對多PK1)
    db_Case_Bidder = db.relationship("bidder_table", backref="case_table")
    # ->Case_table = Bidder_table 關聯性(一對多PK1)

    def __init__(
        self, Case_id, Case_ref_id, Case_Name, Case_Tender_Unit_id,
            Case_Budget_Price, Case_Final_Price, Case_Start_Date,
            Case_End_Date, Case_be_gotten, Case_Company_id):
        self.Case_id = Case_id
        self.Case_ref_id = Case_ref_id
        self.Case_Name = Case_Name
        self.Case_Tender_Unit_id = Case_Tender_Unit_id
        self.Case_Budget_Price = Case_Budget_Price
        self.Case_Final_Price = Case_Final_Price
        self.Case_Start_Date = Case_Start_Date
        self.Case_End_Date = Case_End_Date
        self.Case_be_gotten = Case_be_gotten
        self.Case_Company_id = Case_Company_id


class type_table(db.Model):
    # CREATE TABLE Type_table(
    __table__name = 'type_table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    Type_id = db.Column(db.Integer, primary_key=True, nullable=False)
    # -> Type_id int NOT NULL,
    Type_Name = db.Column(db.String(80), nullable=False)
    # -> type_Name nvarchar(50) NULL,

    db_Type_Company = db.relationship("company_table", backref="type_table")
    # ->Type_table = Company_table 關聯性(一對多PK1)

    def __init__(self, Type_id, Type_Name):
        self.Type_id = Type_id
        self.Type_Name = Type_Name


class tender_unit_table(db.Model):
    # CREATE TABLE Tender_Unit_table(
    __table__name = 'tender_unit_table'  # 建立table名稱，若不寫則看 class name
    # 設定 primary_key
    Tender_Unit_id = db.Column(db.Integer, primary_key=True)
    # -> Tender_Unit_id int NOT NULL,
    Tender_Unit_Name = db.Column(db.String(80), nullable=False)
    # -> Tender_Unit_Name nvarchar(50) NULL,

    db_Tender_Case = db.relationship("case_table", backref="tender_unit_table")
    # ->Tender_Unit_table = Case_table 關聯性(一對多PK1)

    def __init__(self, Tender_Unit_id, Tender_Unit_Name):
        self.Tender_Unit_id = Tender_Unit_id
        self.Tender_Unit_Name = Tender_Unit_Name
    # def __repr__(self):
        # return '<Case_Table %r>' % self.content


@app.route("/", methods=['GET', 'POST'])  # 首頁(找廠商頁面) (.com/(home_page))
def home_index():
    company_type = type_table.query.all()
    return render_template("Buying_net_html_Home.html", company_type=company_type)


@app.route("/case_search", methods=['GET', 'POST'], defaults={"page": 1})  # 找標案頁面 (.com/(result_case))
@app.route("/case_search/<int:page>", methods=['GET', 'POST'])
def case_search(page):
    # company_type = type_table.query.all()
    if request.method == 'POST' or request.method == 'GET':
        filter_case_query = []
        filter_case_query.clear()
        result_data = request.form
        Case_Name = request.form['case_search']
        start_date_begin = request.form['start_date_begin']
        start_date_final = request.form['start_date_final']
        end_date_begin = request.form['end_date_begin']
        end_date_final = request.form['end_date_final']
        price_start = request.form['price_start']
        price_end = request.form['price_end']
        status = request.form['status']
        Company_Name = request.form['company_case_search']
        Tender_Unit_Name = request.form['tender_case_search']

        for key, value in result_data.items():
            if value != '':
                if key == 'case_search':
                    filter_case_query.append(f"Case_Name LIKE '%{value}%'")
                elif key == 'start_date_begin':
                    filter_case_query.append(f"Case_Start_Date>='{value}'")
                elif key == 'start_date_final':
                    filter_case_query.append(f"Case_Start_Date<='{value}'")
                elif key == 'end_date_begin':
                    filter_case_query.append(f"Case_End_Date>='{value}'")
                elif key == 'end_date_final':
                    filter_case_query.append(f"Case_End_Date<='{value}'")
                elif key == 'price_start':
                    filter_case_query.append(f"Case_Final_Price>={value}")
                elif key == 'price_end':
                    filter_case_query.append(f"Case_Final_Price<={value}")
                elif key == 'status':
                    filter_case_query.append(f"Case_be_gotten={value}")
                elif key == 'company_case_search':
                    search_result_company = company_table.query.filter(and_(company_table.Company_Name.contains(f"{value}")))
                    for company_list in search_result_company:
                        filter_case_query.append(f"Case_Company_id={company_list.Company_id}")
                elif key == 'tender_case_search':
                    search_result_tender_unit = tender_unit_table.query.filter(and_(tender_unit_table.Tender_Unit_Name.contains(f"{value}")))
                    for tender_unit_list in search_result_tender_unit:
                        filter_case_query.append(f"Case_Tender_Unit_id={tender_unit_list.Tender_Unit_id}")
            elif value == '' and key == 'company_case_search':
                search_result_company = ''
            elif value == '' and key == 'tender_case_search':
                search_result_tender_unit = ''

        print('filter_case_query: ')
        print(filter_case_query)

        # 標案篩選(原本固定條件篩選)
        if filter_case_query:
            filter_case_query = ' AND '.join(filter_case_query)
            select_query = f"""{filter_case_query}"""
            print(select_query)
            search_result_case = case_table.query.filter(text(select_query))

    return render_template("Buying_net_html_Home.html", search_result_case=search_result_case,
                           Case_Name=Case_Name, Company_Name=Company_Name, Tender_Unit_Name=Tender_Unit_Name, start_date_begin=start_date_begin, start_date_final=start_date_final,
                           end_date_begin=end_date_begin, end_date_final=end_date_final, price_start=price_start, price_end=price_end, status=status, search_way='case')


@app.route("/list_info", methods=['GET', 'POST'])  # 廠商標案頁面
def list_detail():
    if request.method == 'POST' or request.method == 'GET':
        filter_case_query = []
        filter_case_query.clear()
        result_data = request.form
        Case_Name = request.form['case_search']
        start_date_begin = request.form['start_date_begin']
        start_date_final = request.form['start_date_final']
        end_date_begin = request.form['end_date_begin']
        end_date_final = request.form['end_date_final']
        price_start = request.form['price_start']
        price_end = request.form['price_end']
        status = request.form['status']
        Company_Name = request.form['company_case_search']
        Tender_Unit_Name = request.form['tender_case_search']
        print('result_data: ')
        print(result_data)

        for key, value in result_data.items():
            if value != '':
                if key == 'case_search':
                    filter_case_query.append(f"Case_Name LIKE '%{value}%'")
                elif key == 'start_date_begin':
                    filter_case_query.append(f"Case_Start_Date>='{value}'")
                elif key == 'start_date_final':
                    filter_case_query.append(f"Case_Start_Date<='{value}'")
                elif key == 'end_date_begin':
                    filter_case_query.append(f"Case_End_Date>='{value}'")
                elif key == 'end_date_final':
                    filter_case_query.append(f"Case_End_Date<='{value}'")
                elif key == 'price_start':
                    filter_case_query.append(f"Case_Final_Price>={value}")
                elif key == 'price_end':
                    filter_case_query.append(f"Case_Final_Price<={value}")
                elif key == 'status':
                    filter_case_query.append(f"Case_be_gotten={value}")
                # 廠商標案(額外篩選)
                elif key == 'company_case_search':
                    search_result_company = company_table.query.filter(and_(company_table.Company_Name.contains(f"{value}")))
                    search_result_company_count = company_table.query.filter(and_(company_table.Company_Name.contains(f"{value}"))).count()
                    print(search_result_company_count)
                    if search_result_company_count == 1:
                        for company_list in search_result_company:
                            filter_case_query.append(f"Case_Company_id={company_list.Company_id}")
                # 採購單位標案(額外篩選)
                elif key == 'tender_case_search':
                    search_result_tender_unit = tender_unit_table.query.filter(and_(tender_unit_table.Tender_Unit_Name.contains(f"{value}")))
                    search_result_tender_unit_count = tender_unit_table.query.filter(and_(tender_unit_table.Tender_Unit_Name.contains(f"{value}"))).count()
                    print(search_result_tender_unit_count)
                    if search_result_tender_unit_count == 1:
                        for tender_unit_list in search_result_tender_unit:
                            filter_case_query.append(f"Case_Tender_Unit_id={tender_unit_list.Tender_Unit_id}")
            elif value == '' and key == 'company_case_search':
                search_result_company = ''
                search_result_company_count = ''
            elif value == '' and key == 'tender_case_search':
                search_result_tender_unit = ''
                search_result_tender_unit_count = ''
        print('filter_case_query: ')
        print(filter_case_query)

        # 標案篩選(原本固定條件篩選)
        if filter_case_query:
            filter_case_query = ' AND '.join(filter_case_query)
            select_query = f"""{filter_case_query}"""
            print(select_query)
            if search_result_company == '' and search_result_tender_unit == '':
                search_result_case = case_table.query.filter(text(select_query))
                print(search_result_case)
                return render_template("Buying_net_html_Home.html", search_result_case=search_result_case, Case_Name=Case_Name, Company_Name=Company_Name, Tender_Unit_Name=Tender_Unit_Name, start_date_begin=start_date_begin, start_date_final=start_date_final,
                                       end_date_begin=end_date_begin, end_date_final=end_date_final, price_start=price_start, price_end=price_end, status=status, search_way='case')
            elif search_result_company_count == 1 or search_result_tender_unit_count == 1 or (search_result_company_count == 1 and search_result_tender_unit_count == 1):
                search_result_case = case_table.query.filter(text(select_query))
                print(search_result_case)
                return render_template("Buying_net_html_Home.html", search_result_case=search_result_case, Case_Name=Case_Name, Company_Name=Company_Name, Tender_Unit_Name=Tender_Unit_Name, start_date_begin=start_date_begin, start_date_final=start_date_final,
                                       end_date_begin=end_date_begin, end_date_final=end_date_final, price_start=price_start, price_end=price_end, status=status, search_way='case')
        else:
            select_query = ''
    return render_template("Buying_net_html_List.html", select_query=select_query, search_result_company=search_result_company, search_result_tender_unit=search_result_tender_unit,
                           Case_Name=Case_Name, Company_Name=Company_Name, Tender_Unit_Name=Tender_Unit_Name, start_date_begin=start_date_begin, start_date_final=start_date_final,
                           end_date_begin=end_date_begin, end_date_final=end_date_final, price_start=price_start, price_end=price_end, status=status, search_way='case')


@app.route("/case_detail", methods=['GET', 'POST'])  # 採購傷標案頁面
def case_detail():
    if request.method == 'GET':
        compete_list = []
        compete_price = []
        winner_case_list = []
        case_id = request.values.get('cid')
        # 案件詳細資料
        case_detail = case_table.query.filter_by(Case_id=case_id)[0]
        if case_detail.Case_be_gotten == True:
            case_detail.status = u'已結標'
        else:
            case_detail.status = u'尚未結標'

        # 採購單位相關資訊
        tender_detail = tender_unit_table.query.filter_by(Tender_Unit_id=case_detail.Case_Tender_Unit_id)[0]
        tender_case_list = case_table.query.filter_by(Case_Tender_Unit_id=tender_detail.Tender_Unit_id)

        # 競標廠商相關資訊
        company_list = bidder_table.query.filter_by(Bidder_case_id=case_id)
        for company in company_list:
            if company.Bidder_get_case == 1:
                winner_detail = company_table.query.filter_by(Company_id=company.Bidder_company_id)[0]
                winner_cases = bidder_table.query.filter_by(Bidder_company_id=company.Bidder_company_id)
                for case_info in winner_cases:
                    winner_case_list.append(case_table.query.filter_by(Case_id=case_info.Bidder_case_id)[0])
            else:
                compete_list.append(company_table.query.filter_by(Company_id=company.Bidder_company_id)[0])
                compete_price.append(company)
    return render_template("Buying_net_html_Case.html", case_detail=case_detail, tender_detail=tender_detail, tender_case_list=tender_case_list, winner_detail=winner_detail, winner_case_list=winner_case_list, compete_detail=compete_list, compete_price=compete_price)


@app.template_filter()
def currencyFormat(value):
    value = float(value or 0)
    return "{:,.0f}".format(value)


if __name__ == "__main__":
    app.run(debug=True)
