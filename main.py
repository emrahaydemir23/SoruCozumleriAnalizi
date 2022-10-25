import pandas as pd
import streamlit as st
import pandasql as ps
import matplotlib.pyplot as plt

herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1-Uk2ly4wHQqWoohMOpuGMKdUlLhG8B0uQzp88hL8cu8/edit#gid=702254161"
url_1 = herkeseAcikLink.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1)
df['Zaman damgası'] = pd.to_datetime(df['Zaman damgası'])

df1 = df.groupby(["Ders Adı"])[["Doğru Sayısı", "Yanlış Sayısı", "Boş Sayısı", "Çözüm Süresi"]].sum()
#print("Ders Bazlı Toplam Doğru, Yanlış ve Boş Sayıları")
#print(df1.head())

df2 = df.sort_values(by='Zaman damgası', ascending=False)
df2 = df2.groupby(["Ders Adı"])["Zaman damgası"].max()
df2.columns = ["Ders Adı","Son Çözülme Zamanı"]
#print("\n\nDerslerin En Son Çözülme Zamanları")
#print(df2.head())

df3 = df.sort_values(by='Zaman damgası', ascending=False)
df3 = df3.groupby(["Kitap Adı"])["Zaman damgası"].max()
df3.columns = ["Kitap Adı","Son Çözülme Zamanı"]
#print("\n\nKitapların En Son Çözülme Zamanları")
#print(df3.head())


df4 = ps.sqldf("select [Ders Adı], sum([Doğru Sayısı]) as [Doğru Sayısı], sum([Yanlış Sayısı]) as [Yanlış Sayısı], sum([Boş Sayısı]) as [Boş Sayısı], sum([Doğru Sayısı])+sum([Yanlış Sayısı])+sum([Boş Sayısı]) as [ToplamSoruSayisi], (sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3)) as [NetSayisi],(sum([Doğru Sayısı])-(sum([Yanlış Sayısı])/3))*100.0/(sum([Doğru Sayısı])+sum([Yanlış Sayısı])+sum([Boş Sayısı])) as [NetOrani] from df group by [Ders Adı]")
df4 = ps.sqldf("select * from df4 order by [NetOrani]")
ax = df4.plot.bar(x='Ders Adı', y='NetOrani', rot=0)
#plt.show(block=True)



st.set_page_config(page_title="Soru Çözümleri Analizleri", layout="wide", page_icon=":+1:") # https://www.webfx.com/tools/emoji-cheat-sheet/
st.title("SORU ÇÖZÜMLERİ ANALİZLERİ")

st.subheader("Ders Bazlı Toplam Doğru, Yanlış ve Boş Sayıları")
st.write(df1.head())

st.subheader("Ders Bazlı Net Oranları")
st.write(df1.head())

st.subheader("Derslerin En Son Çözülme Zamanları")
st.write(df2.head())

st.subheader("Kitapların En Son Çözülme Zamanları")
st.write(df3.head())

st.subheader("Derslere Göre Net Oranları")
with st.container():
    left, right = st.columns((2,1))#2 birime 1 birim olacak şekilde sütunlara böl
    with left:
        st.write(df4.head())
    with right:
        st.bar_chart(data=df4, x='Ders Adı', y='NetOrani', width=0, height=0, use_container_width=True)


#st.bar_chart(df5)
