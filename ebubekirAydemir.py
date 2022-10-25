import pandas as pd
import streamlit as st
import pandasql as ps
import matplotlib.pyplot as plt

herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1-Uk2ly4wHQqWoohMOpuGMKdUlLhG8B0uQzp88hL8cu8/edit#gid=702254161"
url_1 = herkeseAcikLink.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1)
df["Toplam Sayı"] = df["Doğru Sayısı"]+df["Yanlış Sayısı"]+df["Boş Sayısı"]
df['Zaman damgası'] = pd.to_datetime(df['Zaman damgası'])

df1 = df.groupby(["Ders Adı"])[["Doğru Sayısı", "Yanlış Sayısı", "Boş Sayısı", "Çözüm Süresi"]].sum()

df2 = df.sort_values(by='Zaman damgası', ascending=False)
df2 = df2.groupby(["Ders Adı"])["Zaman damgası"].max()
df2.columns = ["Ders Adı","Son Çözülme Zamanı"]

df3 = df.sort_values(by='Zaman damgası', ascending=False)
df3 = df3.groupby(["Kitap Adı"])["Zaman damgası"].max()
df3.columns = ["Kitap Adı","Son Çözülme Zamanı"]

df4 = ps.sqldf("select [Ders Adı], sum([Doğru Sayısı]) as [Doğru], sum([Yanlış Sayısı]) as [Yanlış], sum([Boş Sayısı]) as [Boş], sum([Doğru Sayısı])+sum([Yanlış Sayısı])+sum([Boş Sayısı]) as [Toplam Soru], (sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3)) as [Net],(sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3))*100.0/(sum([Doğru Sayısı])+sum([Yanlış Sayısı])+sum([Boş Sayısı])) as [Net Oranı] from df group by [Ders Adı]")
df4 = ps.sqldf("select * from df4 order by [Net Oranı]")

df5 = ps.sqldf("select [Ders Adı],[Doğru Sayısı]*100.0/[Toplam Sayı] as [Doğru Oranı],[Yanlış Sayısı]*100.0/[Toplam Sayı] as [Yanlış Oranı],[Boş Sayısı]*100.0/[Toplam Sayı] as [Boş Oranı] from df")

st.set_page_config(page_title="Soru Çözümleri Analizleri", layout="wide", page_icon=":+1:") # https://www.webfx.com/tools/emoji-cheat-sheet/
st.title("EBUBEKİR AYDEMİR")
st.title("SORU ÇÖZÜMLERİ ANALİZLERİ")

st.subheader("Ders Bazlı Toplam Doğru, Yanlış ve Boş Sayıları")
st.write(df1)

st.subheader("Derslerin En Son Çözülme Zamanları")
st.write(df2)

st.subheader("Kitapların En Son Çözülme Zamanları")
st.write(df3)

st.subheader("Derslere Göre Toplam Net Oranları")
with st.container():
    left, right = st.columns((3,2))#2 birime 1 birim olacak şekilde sütunlara böl
    with left:
        st.write(df4)
    with right:
        st.bar_chart(data=df4, x='Ders Adı', y='Net Oranı', width=0, height=0, use_container_width=True)

st.subheader("Derslere Göre Doğru, Yanlış, Boş Oranları")
st.write("Türkçe Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='Türkçe'"))
st.write("Matematik Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='Matematik'"))
st.write("Fen Bilgisi Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='Fen Bilgisi'"))
st.write("Din Kültürü Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='Din Kültürü'"))
st.write("İngilizce Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='İngilizce'"))
st.write("Sosyal Bilgiler Dersi")
st.line_chart(ps.sqldf("select [Doğru Oranı],[Yanlış Oranı],[Boş Oranı] from df5 where [Ders Adı]='Sosyal Bilgiler'"))
