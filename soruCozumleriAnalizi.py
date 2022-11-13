import pandas as pd,datetime
import streamlit as st
import pandasql as ps
import matplotlib.pyplot as plt

herkeseAcikLink, kisiAdi = "", ""
try:
    parametre = st.experimental_get_query_params()
    parametre = parametre["kisi"][0]
    if parametre == "ebubekir":
        herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1-Uk2ly4wHQqWoohMOpuGMKdUlLhG8B0uQzp88hL8cu8/edit#gid=702254161"
        kisiAdi = "EBUBEKİR AYDEMİR"
    elif parametre == "arda":
        herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1JUw8t4WIHo3eUSMQs62cC4RS7LFLnX4Ww8UZnlYv_xM/edit#gid=913864078"
        kisiAdi = "ARDA BULUT"
    elif parametre == "kemal":
        herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1juF8-z_xHQw_FkGRReHCIlezK1QciT-W1dAFLo2SJUY/edit#gid=1046222950"
        kisiAdi = "KEMAL KURT"
    
    url_1 = herkeseAcikLink.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    df["Toplam Sayı"] = df["Doğru Sayısı"]+df["Yanlış Sayısı"]+df["Boş Sayısı"]
    df['Gun'] = pd.to_datetime(df['Zaman damgası'].str[:10], format='%d.%m.%Y')
    df['Zaman damgası'] = pd.to_datetime(df['Zaman damgası'], format='%d.%m.%Y %H:%M:%S')
    genelToplamSure = df["Çözüm Süresi"].sum()

    #df1 = df.groupby(["Ders Adı"])[["Doğru Sayısı", "Yanlış Sayısı", "Boş Sayısı", "Çözüm Süresi"]].sum()

    #df2 = df.sort_values(by='Zaman damgası', ascending=False)
    #df2 = ps.sqldf("Select [Ders Adı],max([Zaman damgası]) as [Zaman],sum([Çözüm Süresi])*1.0/sum([Toplam Sayı]) as [Ortalama Çözüm Süresi], count([Zaman damgası]) as [Çözüm Sayısı],sum([Toplam Sayı]) as [Toplam Soru] from df group by [Ders Adı] order by max([Zaman damgası]) desc")
    #df2['Zaman'] = pd.to_datetime(df2['Zaman'])
    #df2["Geçen Gün Sayısı"] = (datetime.datetime.now()-df2["Zaman"]).dt.days

    #df3 = df.sort_values(by='Zaman damgası', ascending=False)
    #df3 = df3.groupby(["Kitap Adı"])["Zaman damgası"].max()
    #df3.columns = ["Kitap Adı","Son Çözülme Zamanı"]
    #df3 = ps.sqldf("Select [Kitap Adı],max([Zaman damgası]) as [Zaman],sum([Çözüm Süresi])*1.0/sum([Toplam Sayı]) as [Ortalama Çözüm Süresi], count([Zaman damgası]) as [Çözüm Sayısı],sum([Toplam Sayı]) as [Toplam Soru], (sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3))*100.0/(sum([Toplam Sayı])) as [Net Oranı] from df group by [Kitap Adı] order by max([Zaman damgası]) desc")    
    df3 = ps.sqldf(f"Select [Kitap Adı],sum([Doğru Sayısı]) as [Doğru], sum([Yanlış Sayısı]) as [Yanlış], sum([Boş Sayısı]) as [Boş], sum([Toplam Sayı]) as [Toplam], (sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3)) as [Net],(sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3))*100.0/(sum([Toplam Sayı])) as [Net Oranı],sum([Çözüm Süresi]) as [Toplam Süre],sum([Çözüm Süresi])*1.0/sum([Toplam Sayı]) as [Ortalama Süre],sum([Çözüm Süresi])*100.0/{genelToplamSure} as [Toplam Zaman Oranı], count([Zaman damgası]) as [Çözüm Sayısı],max([Zaman damgası]) as [Son Çözüm Zamanı] from df group by [Kitap Adı] order by max([Zaman damgası]) desc")

    df4 = ps.sqldf(f"select [Ders Adı], sum([Doğru Sayısı]) as [Doğru], sum([Yanlış Sayısı]) as [Yanlış], sum([Boş Sayısı]) as [Boş], sum([Toplam Sayı]) as [Toplam], (sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3)) as [Net],(sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3))*100.0/(sum([Toplam Sayı])) as [Net Oranı],sum([Çözüm Süresi]) as [Toplam Süre],sum([Çözüm Süresi])*1.0/sum([Toplam Sayı]) as [Ortalama Süre],sum([Çözüm Süresi])*100.0/{genelToplamSure} as [Toplam Zaman Oranı], count([Zaman damgası]) as [Çözüm Sayısı],max([Zaman damgası]) as [Son Çözüm Zamanı] from df group by [Ders Adı] order by max([Zaman damgası]) desc")
    df4 = ps.sqldf("select * from df4 order by [Net Oranı]")

    df5 = ps.sqldf("select [Ders Adı],[Doğru Sayısı]*100.0/[Toplam Sayı] as [Doğru Oranı],[Yanlış Sayısı]*100.0/[Toplam Sayı] as [Yanlış Oranı],[Boş Sayısı]*100.0/[Toplam Sayı] as [Boş Oranı] from df")

    df6 = ps.sqldf("Select Gun as [Gün],sum([Toplam Sayı]) as [Toplam Sayı] from df group by Gun order by Gun desc")
    
    genelToplamSure = df["Çözüm Süresi"].sum()
    genelToplamGun = len(pd.unique(df['Gun']))
    genelToplamSoru = df["Toplam Sayı"].sum()
    genelToplamKitapSayisi = len(pd.unique(df['Kitap Adı']))
    df7 = pd.DataFrame({'Türü': pd.Series(dtype='str'), 'Değer': pd.Series(dtype='str')})
    df7.loc[len(df7.index)] = ['Toplam Süre', '{:02d}:{:02d}'.format(*divmod(genelToplamSure, 60))]
    df7.loc[len(df7.index)] = ['Günlük Ortalama Süre', '{:02d}:{:02d}'.format(*divmod(int(genelToplamSure/genelToplamGun), 60))]
    df7.loc[len(df7.index)] = ['Toplam Soru', genelToplamSoru]
    df7.loc[len(df7.index)] = ['Toplam Gün', genelToplamGun]
    df7.loc[len(df7.index)] = ['Toplam Kitap', genelToplamKitapSayisi]
    df7.loc[len(df7.index)] = ['Ortalama Net Oranı', df3["Net Oranı"].mean()]
    df7.loc[len(df7.index)] = ['Son Çözüm Zamanı', df["Zaman damgası"].max()]
    df7.loc[len(df7.index)] = ['En Eski Çözülen Kitap', df3.sort_values(by=['Son Çözüm Zamanı'],ascending=False).iloc[-1]["Kitap Adı"]]
    df7.loc[len(df7.index)] = ['En Az Soru Çözülen Kitap', df3.sort_values(by=['Toplam'],ascending=False).iloc[-1]["Kitap Adı"]]
    
    st.set_page_config(page_title="Soru Çözümleri Analizleri", layout="wide", page_icon=":+1:") # https://www.webfx.com/tools/emoji-cheat-sheet/
    st.title(kisiAdi)
    st.title("SORU ÇÖZÜMLERİ ANALİZLERİ")
    
    st.subheader("Genel Bilgiler")
    st.write(df7)
    
    st.subheader("Ders Net Oranları")
    st.bar_chart(data=df4, x='Ders Adı', y='Net Oranı', width=0, height=0, use_container_width=True)       
    
    st.subheader("Derslere Göre Detaylı Analizler")
    st.write(df4)
    #with st.container():
        #left, right = st.columns((3,2))#2 birime 1 birim olacak şekilde sütunlara böl
        #with left:
            #st.write(df4)
        #with right:
            #st.bar_chart(data=df4, x='Ders Adı', y='Net Oranı', width=0, height=0, use_container_width=True)
    
    st.subheader("Kitaplara Göre Detaylı Analizler")
    st.write(df3)
    
    st.subheader("Günlere Göre Toplam Soru Sayıları")
    st.line_chart(df6,x='Gün', y='Toplam Sayı')

    st.subheader("Derslere Göre Doğru, Yanlış, Boş Oranları")
    df6 = ps.sqldf("Select distinct [Ders Adı] from df")
    for index, row in df6.iterrows():
        st.write(row['Ders Adı'])
        st.line_chart(ps.sqldf(f"select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='{row['Ders Adı']}'"))
    
    st.print(sidebar=False, printer="PDF")
except:
    pass

