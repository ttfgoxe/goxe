from pickle import TRUE
import smtplib
from xmlrpc.client import TRANSPORT_ERROR
import numpy as np
from logging import error
from mimetypes import MimeTypes
import streamlit as st
import email, smtplib, ssl # to automate email
import email as mail
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime as dt # to work with date, time
from bs4 import BeautifulSoup # to work with web scrapping (HTML)
import pandas as pd # to work with tables (DataFrames) data
from IPython.core.display import HTML
from streamlit.elements import multiselect # to display HTML in the notebook
import PIL
from email.utils import make_msgid
import mimetypes

st.set_page_config(layout='wide')

def ncc_f():
    import streamlit as st
    import pandas as pd
    from google.oauth2 import service_account
    import gspread #-> Để update data lên Google Spreadsheet
    from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
    # from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
    )
    gc = gspread.authorize(credentials)
    spreadsheet_key='1KBTVmlT5S2_x9VGseHdk_QDvZIfNBOLJy78lM0p3ORQ'

    sh=gc.open('Kho NVL - NCC').worksheet('Sheet1')
    sheet=sh.get_all_values()
    ncc=pd.DataFrame(sheet)
    ncc.columns=ncc.iloc[0]
    ncc=ncc[1:]
    # ncc
    A = ncc['TÊN NCC'].tolist()
    B= ncc['MÃ'].tolist()
    return A,B
abv=ncc_f()
list_ncc=abv[0]
list_int=abv[1]
from list_info import qc_list
go_list=["ALDER",
"ASH VN","ASH","BẠCH ĐÀN","BEECH","CĂM XE","CAO SU ĐEN","CAO SU","CHERRY","CHÒ CHỈ","SYCAMORE","DỪA","DƯƠNG LIỄU","GÒN","HICKORY","KAPUS","LÒNG MỨT","MAPLE","MÍT","MUỒNG","NEP PALLET","OAK","PƠ MU","POPLAR","RED ELM","RED OAK","SỌ KHỈ",
"TẠP","TEAK","THÔNG","TRÀM","TRÅU","WALNUT","WHITE OAK","WHITE POPLAR","WILLOW","XOÀI"]
in_list=["ADL","ASV","ASH","BDA","BEE","CXE","CSD","CSU","CHE","CCI","SYC","DUA","DLI","GON","HIC","KAP","LMU","MAP","MIT","MNG","NPL","OAK","PMU","PLR","REL","ROK","SOK","TAP","TEK","THO","TRM","TRU","WAL","WOK","WPR","WIL","XOA"]
# abv


import barcode
from barcode.writer import ImageWriter
def qr_code(link="https://engineering.catholic.edu/eecs/index.html"):
        ean = barcode.get('code128', link, writer=ImageWriter())
        filename = ean.save('code128',{"module_width":0.2, "module_height":4.7, "font_size":7, "text_distance": 2, "quiet_zone": 1})
        return filename

def send_email(subject,total,tk,QC,NCC,qc,ml,td,html,receiver_list,dm):
    # (1) Create the email head (sender, receiver, and subject)
    sender_email = st.secrets['SENDER_EMAIL']
    password = st.secrets['PWD_EMAIL']
    # receiver_email='hieulam1312@gmail.com'
    email = MIMEMultipart()
    email["From"] = sender_email
    # email["To"] = 'abc'
    email['Subject']=subject

   # email.attach(msgImage)
    fp = open('code128.png', 'rb')
    img = MIMEImage(fp.read())
    img.add_header('Content-Disposition', 'attachment', filename='code128.png')
    img.add_header('X-Attachment-Id', '0')
    img.add_header('Content-ID', '<0>')
    fp.close()
    email.attach(img)

    # Attach HTML body
    email.attach(MIMEText(
        '''
        <html>
                <h1 style="text-align: center;">THẺ KIỆN  NGÀY {}    <h1>
                <img src="cid:0">
                <h3>Tổng số khối:     {}   &nbsp;    &nbsp;  QC kiểm: {}  &nbsp;  &nbsp;   Mã lô: {}                &nbsp;  &nbsp;               &nbsp; &nbsp;            Độ ẩm:{} <h3>
        </html>
        '''.format(td,total,qc,ml,dm),
        'html', 'utf-8'))
    part1 = MIMEText(html, 'html')
    email.attach(part1)
    try:
        session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
        session.starttls() #enable security
        session.login(sender_email, password) #login with mail_id and password
    
        for receiver_email in receiver_list:
            email['To'] = receiver_email
            text = email.as_string()
            session.sendmail(sender_email, receiver_email, text)
        st.success('Đã gửi mail thành công')
        return(1)
    except:
        print("Could not send mail to")
        return(0)

def eccount(df):
    df4=df.copy()
    uni_tk=df4['THẺ KIỆN'].unique().tolist()
    uni_dai=df4['Dài'].unique().tolist()
    uni_dai.sort()
    if len(uni_dai)==2:

        string_dai=str(int(uni_dai[0]))+"/"+str(int(uni_dai[-1]))
    elif len(uni_dai)==1:
        string_dai=str(int(uni_dai[0]))
    else:

        string_dai=str(int(uni_dai[0]))+"-"+str(int(uni_dai[-1]))
    df4['DÀI 2']=string_dai
    df4['THẺ KIỆN2']=tk
    df4['THẺ KIỆN 3']=tk
    df4['Dày2']=df['Dày']
    df4["ncc"]=ini
    df4['Loại Gỗ']=in_list[go_list.index(go[0])]
    eccount=df4[['THẺ KIỆN','THẺ KIỆN2','THẺ KIỆN 3','Dày','DÀI 2','Mã lô','Loại Gỗ','Dày2','ncc','SỐ KHỐI']]

    eccount_gr=eccount.groupby(['THẺ KIỆN','THẺ KIỆN2','THẺ KIỆN 3','Dày','DÀI 2','Mã lô','Loại Gỗ','Dày2','ncc'])['SỐ KHỐI'].sum().reset_index()
    return eccount_gr

def pull_data():
    #Library to call Google API
    from google.oauth2 import service_account
    import gspread #-> Để update data lên Google Spreadsheet
    from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet 
    #Call Credetials
    credentials=service_account.Credentials.from_service_account_info(
        st.secrets['gcp_service_account'],
        scopes=['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'],)

    gc=gspread.authorize(credentials)
    sh=gc.open('Kho NVL - NCC').worksheet('Sheet2')
    sheet=sh.get_all_records()
    df=pd.DataFrame(sheet).astype(str)
    
    return df    

def push(df,str):
    import streamlit as st
    import pandas as pd
    from google.oauth2 import service_account
    import gspread #-> Để update data lên Google Spreadsheet
    from gspread_dataframe import set_with_dataframe #-> Để update data lên Google Spreadsheet
    from oauth2client.service_account import ServiceAccountCredentials #-> Để nhập Google Spreadsheet Credentials
    credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive'],
    )
    gc = gspread.authorize(credentials)
    spreadsheet_key='1KBTVmlT5S2_x9VGseHdk_QDvZIfNBOLJy78lM0p3ORQ'

    import gspread_dataframe as gd
    import gspread as gs

    ws = gc.open("Kho NVL - NCC").worksheet(str)
    existing = gd.get_as_dataframe(ws)
    # existing
    updated = existing.append(df)
    gd.set_with_dataframe(ws, updated)
    st.success('Bấm Xóa nội dung thẻ kiện cũ để tiếp tục')

st.subheader('Nhập thông tin:')

# st.set_page_config(layout='wide')

a2,a3,a4,a5,a6=st.columns((1.5,1.5,1,1,1))
with a2:
    ncc=st.multiselect('NCC:',list_ncc)
with a3:
    qc=st.multiselect('QC kiểm:',qc_list)
with a4:
    go=st.multiselect('Loại gỗ:',go_list)
with a6:
    da=st.text_input('Độ ẩm:',)
with a5:
    clg=st.text_input('Chất lượng gỗ',)
cls1,cls2,cls3=st.columns(3)
with cls1:
    tk1=st.number_input('Thẻ Kiện:',step=1)
with cls2:
    ml=st.text_input('Mã lô:',)
if 'count' not in st.session_state:
    st.session_state.count = 0

def increment_counter(increment_value=0):
    st.session_state.count += increment_value

def decrement_counter(decrement_value=0):
    st.session_state.count -= decrement_value

c1,c2,c3,c4,c5=st.columns((1,1,1,2,2))
with c1:
    st.button('Thêm dòng', on_click=increment_counter,
        kwargs=dict(increment_value=5))
with c2:
    st.button('Giảm dòng', on_click=decrement_counter,
        kwargs=dict(decrement_value=1))
with c4:
    st.write('Tổng số dòng = ', st.session_state.count+1)
h=st.session_state.count


if not ncc:
    st.info('Nhập đầy đủ thông tin ở phía trên')
else:
    st.subheader('Danh sách kiểm chi tiết:')

    placeholder = st.empty()

    with placeholder.container():
    # dv=st.selectbox('Đơn vị đo:',['mm','Inch','feet'])
        with st.form(key='columns_in_form'):


            r1,r2,r3,r4=st.columns(4)
            with r1:
                a=r1.number_input('Dày',)
            with r3:
                with placeholder.container():
                    b=[]
                    for nr in range(5+st.session_state.count):                 
                        b.append(r3.number_input(label='Rộng', key=f'2`1 {nr}'))
            with r2:
                    c=st.number_input('Dài',step=1)
            with r4:            
                # placeholder2 = r4.empty()
                with placeholder.container():
                    d=[]
                    for nr in range(5+st.session_state.count):
                        
                        d.append(r4.number_input(label='Số thanh', key=f'Quesdfgtion {nr}',step=1))
            # click_clear = st.checkbox('clear text input', key=1)

                
            st.form_submit_button('submit')

#         b=["0" if v =="" else v for v in b]
#         # c=["0" if v =="" else v for v in c]
#         d=["0 "if v =="" else v for v in d]

#         b1=[]
#         c1=[]


#         for b_ in b:
#             new_string = b_.replace(',','.')
#             b1.append(new_string)

        ncc_index=list_ncc.index(ncc[0])
        ini=list_int[ncc_index]

        dict={'Rộng':b,'Số thanh':d}
    
        import pandas as pd
        df=pd.DataFrame.from_dict(dict)    
#         df=df.astype(float)
        df['Rộng']=round(df['Rộng'],2)
        df['Dài']=round(float(c),2)
        df['Dày']=round(float(a),2)

        khoi=df['Dày']*df['Rộng']*df['Dài']*df['Số thanh']

        df['SỐ KHỐI']=round(khoi/10**9,4)
        td=pd.to_datetime('today').date()
        df['NGÀY KIỂM']=td
        # df['THẺ KIỆN']=tk
        df['NCC']=ncc[0]
        df['LOẠI GỖ']=go[0]
        df['QC KIỂM']=qc[0]

        total=round(sum(df['SỐ KHỐI']),4)
        df=df[df['SỐ KHỐI']>0]
        d1=df.sort_index(ascending=False).reset_index(drop=True)      
        #Cân đối số liệu
        # _du=0
        st.subheader('Cân đối số liệu')
        cl1,cl2=st.columns(2)
        with cl1:
            ncc_num=st.number_input('Số khối NCC:',format="%.4f")
        with cl2: 
            st.write('**Tổng số khối thực kiểm:** ',total)
            
            _du=total-ncc_num

            if _du>0.001:

                _row0=d1.head(1)
                stt=_row0['Số thanh'].tolist()
                sk=(_row0['Dày']*_row0['Rộng']*_row0['Dài']*_row0['Số thanh'])/10**9

                test=((_du)*(10**9))/(_row0['Dày']*_row0['Rộng']*_row0['Dài'])
                # _row0['Số thanh']
                # 
                st.write('**Điều chỉnh số thanh mã cuối cùng thành:**',stt[0]-round(test[0],0))

        st.subheader('KẾT QUẢ:')

        c1,c2=st.columns(2)
        with c1:
            tk="K."+in_list[go_list.index(go[0])]+"."+str(tk1)
            st.write('**Thẻ kiện:** ',tk)
            st.write('**Mã lô:** ',ml)
            NCC=ncc[0]+" "+"("+clg+")"
            st.write('**NCC:** ',NCC)
        df['THẺ KIỆN']=tk
        df['Mã lô']=ml
        df['NCC']=NCC
        df['ĐỘ ẨM']=da
        # with c2:
        #    image= image=st.image(qr_code(link=tk))
        df=df[['Dày','Rộng','Dài','Số thanh','SỐ KHỐI','NGÀY KIỂM'	,'NCC',	'LOẠI GỖ',	'QC KIỂM',	'THẺ KIỆN',	'Mã lô',	'ĐỘ ẨM']]

        
        #XUẤT THẺ KIỆN

    def xuat(ma_tk):
        data=pull_data()
        df=data[data['THẺ KIỆN']==ma_tk].reset_index(drop=True)
        df['SỐ KHỐI']=df['SỐ KHỐI'].astype(float)
        df2=df[['Dày','Rộng','Dài','Số thanh','SỐ KHỐI']]

        df2['Số thanh']=df2['Số thanh'].astype(int)
        df2['SỐ KHỐI']=df2['SỐ KHỐI'].astype(str)
        
        df2=df2.astype(str)
        df2=df2.replace("0"," ")
        df2=df2.replace("0.0"," ")
        df
        # df2
        st.write('**Tổng số khối:** ',round(sum(df['SỐ KHỐI']),4))

        len_=len(df.index.tolist())

        if len_<51 and len_>25:    
            df_20=df2.iloc[:25]
            df_20=df_20.astype(str)
            df_20['Dày']=df_20['Dày'].str.replace(".",",")
            df_20['Dày']=df_20['Dày'].str.replace(",0","")
            
            df_20['Rộng']=df_20['Rộng'].str.replace(".",",")
            df_20['Rộng']=df_20['Rộng'].str.replace(",0","")
            df_20['Dài']=df_20['Dài'].str.replace(".",",")
            df_20['Dài']=df_20['Dài'].str.replace(",0","")

            df_o=df_20.copy()
            df_o=df_o.notnull()
            df_o=df_o.replace(True,0)
        

            df_ov=df2.iloc[25:].reset_index(drop=True)
   
            df_o.loc[df_ov.index, :] = df_ov[:]
            df_o=df_o.astype(str)
            df_o=df_o.replace("0",".")
            df_o['Dày']=df_o['Dày'].str.replace(".",",")
            df_o['Dày']=df_o['Dày'].str.replace(",0","")
            # df22
            df_o['Rộng']=df_o['Rộng'].str.replace(".",",")
            df_o['Rộng']=df_o['Rộng'].str.replace(",0","")
            df_o['Dài']=df_o['Dài'].str.replace(".",",")
            df_o['Dài']=df_o['Dài'].str.replace(",0","")           
            df_over=df_o.copy()

            # df_over=df_0.loc[df1.index, :] = df1[:]
            html = """ DANH SÁCH THẺ KIỆN\n
                    <body> 
                    <table  margin-bottom= "2000" cellpadding="2" cellspacing="2" padding="10">     
                    <tr>         
                    <td>             
                    <table  margin-bottom= "2000" cellpadding="2" cellspacing="2" padding="10">                  
                    <tr>                     
                    <td>{0}<td> 
                    <td>{1}</td>                 
                    </tr>             
                    </table>         
                    </td>     
                    </tr> 
                    </table> 
                    </body>
                        """.format(df_20.to_html(index=False,col_space=50),df_over.to_html(index=False,col_space=50))
        elif len_>50:
            df_20=df2.iloc[:25]
            df_20=df_20.astype(str)
            df_20['Dày']=df_20['Dày'].str.replace(".",",")
            df_20['Dày']=df_20['Dày'].str.replace(",0","")
            
            df_20['Rộng']=df_20['Rộng'].str.replace(".",",")
            df_20['Rộng']=df_20['Rộng'].str.replace(",0","")
            df_20['Dài']=df_20['Dài'].str.replace(".",",")
            df_20['Dài']=df_20['Dài'].str.replace(",0","")
            # df_20
            df_o=df_20.copy()
            df_o=df_o.notnull()
            df_o=df_o.replace(True,0)

            df_ov=df2.iloc[25:50].reset_index(drop=True)
   
            df_o.loc[df_ov.index, :] = df_ov[:]
            df_o=df_o.astype(str)
            df_o=df_o.replace("0",".")
            df_o['Dày']=df_o['Dày'].str.replace(".",",")
            df_o['Dày']=df_o['Dày'].str.replace(",0","")
            # df22
            df_o['Rộng']=df_o['Rộng'].str.replace(".",",")
            df_o['Rộng']=df_o['Rộng'].str.replace(",0","")
            df_o['Dài']=df_o['Dài'].str.replace(".",",")
            df_o['Dài']=df_o['Dài'].str.replace(",0","")           
            df_over=df_o.copy()



            df_50=df2.iloc[51:]
            df_50=df_50.astype(str)
            df_50['Dày']=df_50['Dày'].str.replace(".",",")
            df_50['Dày']=df_50['Dày'].str.replace(",0","")
            
            df_50['Rộng']=df_50['Rộng'].str.replace(".",",")
            df_50['Rộng']=df_50['Rộng'].str.replace(",0","")
            df_50['Dài']=df_50['Dài'].str.replace(".",",")
            df_50['Dài']=df_50['Dài'].str.replace(",0","")



            # df_over=df_0.loc[df1.index, :] = df1[:]
            html = """ DANH SÁCH THẺ KIỆN 1/2\n
                    <body> 
                    <table  margin-bottom= "2000" cellpadding="2" cellspacing="2.2" padding="10">     
                    <tr>         
                    <td>             
                    <table  margin-bottom= "2000" cellpadding="2" cellspacing="2.2" padding="10">                  
                    <tr>                     
                    <td>{0}<td> 
                    <td>{1}</td>                 
                    </tr>  
                    <br>
                    <br>
                    <br>
                    <br>
                    </body>
                    DANH SÁCH THẺ KIỆN 2/2
                    <body>
                        {2}
                        <br>
                    </body>
                        """.format(df_20.to_html(index=False,col_space=60),df_over.to_html(index=False,col_space=60),df_50.to_html(index=False,col_space=120,justify='center'))



        else:

            df22=df2.copy()
            # df22=df22.astype(str)
            df22['Dày']=df22['Dày'].str.replace(".",",")
            df22['Dày']=df22['Dày'].str.replace(",0","")
            # df22
            df22['Rộng']=df22['Rộng'].str.replace(".",",")
            df22['Rộng']=df22['Rộng'].str.replace(",0","")
            df22['Dài']=df22['Dài'].str.replace(".",",")
            df22['Dài']=df22['Dài'].str.replace(",0","")
            # df22
            # df22['Dài']=df22['Dài'].str.replace(".0"," ")
            df22.columns= df22.columns.str.replace('.','',regex=True)
            
            html = """ DANH SÁCH THẺ KIỆN\n
                    <html>
                    <br>
                    <head></head>
                    <body>
                        {0}
                        <br>
                    </body>
                    </html>
                    """.format(df22.to_html(index=False,col_space=100,justify='center'))
        return html,df,round(sum(df['SỐ KHỐI']),4)

    list_email=['qlcl@tanthanhgroup.com']
    st.info('Sau mỗi quy cách dài thì bấm lưu thông tin để lưu lại, tránh trường hợp bị xóa mất. Lưu xong thì bấm Xóa nội dung kiện cũ, nhập thêm quy cách dài mới và tiếp tục bấm lưu thông tin cho đến khi xong')
    if st.button('Lưu thông tin'):
        df['NGÀY KIỂM']=df['NGÀY KIỂM'].astype(str)

        push(df,'Sheet2')
    if st.button("Xóa nội dung thẻ kiện cũ"):
        placeholder.empty()
    st.info('Sau khi nhập liệu xong toàn bộ thẻ kiện, bấm Tạo thẻ kiện để hoàn thành')
    if st.button('Tạo thẻ kiện'):
        list_dt=xuat(tk)
#         list_dt[0]
        send_email("Thẻ kiện: "+tk+" - "+NCC+" - "+qc[0],list_dt[2],tk,qr_code(link=tk),NCC,qc[0],ml,td,list_dt[0],list_email,da)
        sheet='Ecount'
        # from cv import push
        ECC=eccount(list_dt[1])
        push(ECC,sheet)
