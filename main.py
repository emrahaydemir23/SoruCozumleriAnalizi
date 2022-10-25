import pandas as pd
import streamlit as st

herkeseAcikLink = "https://docs.google.com/spreadsheets/d/1-Uk2ly4wHQqWoohMOpuGMKdUlLhG8B0uQzp88hL8cu8/edit#gid=702254161"
url_1 = herkeseAcikLink.replace('/edit#gid=', '/export?format=csv&gid=')
df = pd.read_csv(url_1)

df1 = df.groupby(["Ders Adı"])[["Doğru Sayısı", "Yanlış Sayısı", "Boş Sayısı", "Çözüm Süresi"]].sum()
#print("Ders Bazlı Toplam Doğru, Yanlış ve Boş Sayıları")
#print(df1.head())

df['Zaman damgası'] = pd.to_datetime(df['Zaman damgası'])
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

#df4 = df1.copy()
#df4["Net Sayısı"] = df4["Doğru Sayısı"] - (df4["Yanlış Sayısı"]/3)
#df4["Net Oranı"] = df4["Net Sayısı"] / (df4["Doğru Sayısı"] + df4["Yanlış Sayısı"] + df4["Boş Sayısı"])
#df4 = df4.drop(['Net Sayısı', 'Doğru Sayısı' , 'Yanlış Sayısı' , 'Boş Sayısı'], axis=1)
#ax = df4.plot.bar(x='Ders Adı', y='Net Oranı', rot=0)

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
