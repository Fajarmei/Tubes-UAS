import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from streamlit_option_menu import option_menu
# from streamlit_extras.stylable_container import stylable_container

stylecss = """
<style>

# [data-testid="stVerticalBlockBorderWrapper"]{
#     background-color:blue;
# }

[data-testid="stImage"]{
    width:150px;
    display:block;
    margin:0 auto;
}

[data-testid="column"]{
    background-color:#fff;
    border-radius:20px;
    text-align:center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

[data-testid="stMarkdown"] .titleData {
    margin:2vh 0px 0px 0px;
    padding:0px;
    line-height:20px;
    color:black;
}
[data-testid="stMarkdown"] .nilaiData-1, .nilaiData-2, .nilaiData-3 {
    font-size:40px;
    padding:0px;
    font-weight:600;
    margin:0vh 0px 0px 0px;
    line-height:60px;
    color:black;
}

[data-testid="stMarkdown"] .nilaiData-1 {
    color:green;
}
[data-testid="stMarkdown"] .nilaiData-2 {
    color:red;
}
[data-testid="stMarkdown"] .namaKota {
    line-height:1px;
    margin-bottom:7vh;
    color:black;
}



body {
    background-color: #0000;  /* Replace with your desired background color code */
}
</style>
"""

st.markdown(stylecss, unsafe_allow_html=True)


#WRANGLING
# Kategori produk dengan penjualan terbanyak
df_order = pd.read_csv('order_items_dataset.csv')
df_product = pd.read_csv('products_dataset.csv')
df_category_name = pd.read_csv('product_category_name_translation.csv')
df_sellers = pd.read_csv('sellers_dataset.csv')
geolocation_df = pd.read_csv('geolocation_dataset.csv')

#CLEANING
#Format Missing Value
missing_value_format = ['N.A', 'na', 'n.a.','n/a','?','-']

#Tambahkan parameter na_values untuk memformat missing values
df_order = pd.read_csv('order_items_dataset.csv', na_values = missing_value_format)
df_product = pd.read_csv('products_dataset.csv', na_values = missing_value_format)
df_category_name = pd.read_csv('product_category_name_translation.csv', na_values = missing_value_format)
df_sellers = pd.read_csv('sellers_dataset.csv', na_values = missing_value_format)

nan = df_product.isna().sum().index #Memeriksa jumlah missing values di tiap kolom
df_product.dropna(subset= nan, axis=0, inplace=True) #Menghapus baris memiliki null
df_product.reset_index(drop=True, inplace=True) #Reset index

#NOMOR 2
df_seller_city = df_sellers.groupby('seller_city')['seller_id'].count()
most_sellers = df_seller_city.sort_values(ascending=True).tail(10)

#MERGING DATA
df_merged = pd.merge(df_product,df_category_name, how='left', on='product_category_name')
df_merged2 = pd.merge(df_order, df_merged, how='left', on='product_id')
df_full = pd.merge(df_merged2, df_sellers, how='left', on='seller_id')
hapus = ['seller_id','shipping_limit_date','price','freight_value','product_name_lenght','product_description_lenght','product_photos_qty','product_weight_g','product_length_cm','product_height_cm','product_width_cm','seller_zip_code_prefix','seller_state','product_category_name']
df_full.drop(hapus, axis=1, inplace=True)
produk_terjual = df_full.groupby('product_category_name_english')['order_item_id'].sum()


# ================================= START SIDEBAR =================================
with st.sidebar:
    image_path = 'logo_scikit.png'
    st.image(image_path)

    selected = option_menu('Menu',['Dashboard'],
    icons =["easel2", "graph-up"],
    menu_icon="cast",
    default_index=0)


# ================================= END SIDEBAR =================================


# ================================= START CONTENT =================================


#Inisiasialisasi title data yang akan ditampilkan 
opt1 = "Data customer di berbagai kota"
opt2 = "Data seller di berbagai kota"
opt3 = "Data metode pembayaran yang sering digunakan"
opt4 = "Data rating produk di berbagai kategori"

#Selectbox untuk memilih data yang akan dianalisis
option = st.selectbox(
    label="Pilih data yang akan di analisis",
    options=(opt1, opt2, opt3, opt4)
)

# df = pd.read_csv("E-Commerce Public Dataset\customers_dataset.csv")

if option == opt1:

    file_path       = 'customers_dataset.csv' 
    df              = pd.read_csv(file_path)    
    st.subheader('Data customer di berbagai kota')
    col1, col2, col3 = st.columns(3)

    with col1:    
        terbanyak_teks  = df['customer_city'].value_counts().idxmax()    
        terbanyak_angka  = df['customer_city'].value_counts().max()      
        output_terbanyak = f"<p class='titleData'>Highest</p><p class='nilaiData-1'>{terbanyak_angka}</p><p class='namaKota'>Customer in {terbanyak_teks}</p>"    
        st.markdown(output_terbanyak, unsafe_allow_html=True) 
        

    with col2:     
        terkecil_teks  = df['customer_city'].value_counts().idxmin()    
        terkecil_angka  = df['customer_city'].value_counts().min()    
        output_terkecil = f"<p class='titleData'>Lowest</p><p class='nilaiData-2'>{terkecil_angka}</p><p class='namaKota'>Customer in {terkecil_teks}</p>"    
        st.markdown(output_terkecil, unsafe_allow_html=True)      

    with col3:       
        rata_angka  = df['customer_city'].count()    
        output_rata = f"<p class='titleData'>Total</p><p class='nilaiData-3'>{rata_angka}</p><p class='namaKota'>Customer</p>"    
        st.markdown(output_rata, unsafe_allow_html=True)   


    customer_city_dist = df['customer_city'].value_counts()
    customer_city_dist = customer_city_dist.reset_index()
    customer_city_dist.columns = ['customer_city', 'Count']

    with st.container():
        values = st.slider(
            label='Select a range of values',
            min_value=0,
            max_value=5,
            value=5
        )

        # st.write('Values:', values)


        # st.write(customer_city_dist)
        customer_city_dist = customer_city_dist.head(values)
        fig = px.pie(customer_city_dist, values='Count', names='customer_city')
        st.write(fig)
    with st.expander("Penjelasan Data Customer di Setiap Kota")   :
            st.write('Dilihat dari grafik diatas, Customer terbanyak berada di kota sao paulo, kedua berada di kota rio de janeiro, ketiga berada di kota belo horizonte, keempat berada di kota brasilia dan terakhir di kota curitiba.')

elif option == opt2:

    file_path       = 'E-Commerce Public Dataset\sellers_dataset.csv' 
    df              = pd.read_csv(file_path)  
    st.subheader('Data seller di berbagai kota')
    col1, col2, col3 = st.columns(3)

    with col1:    
        terbanyak_teks  = df['seller_city'].value_counts().idxmax()    
        terbanyak_angka  = df['seller_city'].value_counts().max()      
        output_terbanyak = f"<p class='titleData'>Highest</p><p class='nilaiData-1'>{terbanyak_angka}</p><p class='namaKota'>Seller in {terbanyak_teks}</p>"    
        st.markdown(output_terbanyak, unsafe_allow_html=True)    
        # st.write('Jumlah = ', terbanyak_angka, "customer")

    with col2:     
        terkecil_teks  = df['seller_city'].value_counts().idxmin()    
        terkecil_angka  = df['seller_city'].value_counts().min()    
        output_terkecil = f"<p class='titleData'>Lowest</p><p class='nilaiData-2'>{terkecil_angka}</p><p class='namaKota'>Seller in {terkecil_teks}</p>"    
        st.markdown(output_terkecil, unsafe_allow_html=True)      

    with col3:       
        rata_angka  = df['seller_city'].count()    
        output_rata = f"<p class='titleData'>Total</p><p class='nilaiData-3'>{rata_angka}</p><p class='namaKota'>Seller</p>"    
        st.markdown(output_rata, unsafe_allow_html=True)   


    seller_city_dist = df['seller_city'].value_counts()
    seller_city_dist = seller_city_dist.reset_index()
    seller_city_dist.columns = ['seller_city', 'Count']

    with st.container():
        values = st.slider(
            label='Select a range of values',
            min_value=0,
            max_value=5,
            value=5
        )

        # st.write('Values:', values)


        # st.write(seller_city_dist)
        seller_city_dist = seller_city_dist.head(values)
        fig = px.pie(seller_city_dist, values='Count', names='seller_city')
        st.write(fig)
        
    with st.expander("Penjelasan data Seller di setiap Kota") :
        st.write("Berdasarkan hasil analisis data yang telah dilakukan dapat disimpulkan bahwa 10 kota dengan seller terbanyak berada di kota:")
        st.write("- Sao Paulo")
        st.write("- Curitiba")
        st.write("- Rio de Janeiro")
        st.write("- Belo Horizonte")
        st.write("- Ribeirao Preto")
        st.write("- Guarulhos")
        st.write("- Ibitinga")
        st.write("- Santo Andre")
        st.write("- Campinas")
        st.write("- Maringa")

elif option == opt3:


    file_path       = 'E-Commerce Public Dataset\order_payments_dataset.csv' 
    df              = pd.read_csv(file_path) 
    df              = df[df['payment_type'] != 'not_defined']
    st.subheader('Data metode pembayaran yang sering digunakan')
    col1, col2, col3 = st.columns(3)

    with col1:    
        terbanyak_teks  = df['payment_type'].value_counts().idxmax()    
        terbanyak_angka  = df['payment_type'].value_counts().max()      
        output_terbanyak = f"<p class='titleData'>Highest</p><p class='nilaiData-1'>{terbanyak_angka}</p><p class='namaKota'>Cust. using {terbanyak_teks}</p>"    
        st.markdown(output_terbanyak, unsafe_allow_html=True)    
        # st.write('Jumlah = ', terbanyak_angka, "customer")

    with col2:     
        terkecil_teks  = df['payment_type'].value_counts().idxmin()    
        terkecil_angka  = df['payment_type'].value_counts().min()    
        output_terkecil = f"<p class='titleData'>Lowest</p><p class='nilaiData-2'>{terkecil_angka}</p><p class='namaKota'>Cust. using {terkecil_teks}</p>"    
        st.markdown(output_terkecil, unsafe_allow_html=True)      

    with col3:       
        total_angka  = df['payment_type'].count()    
        output_total = f"<p class='titleData'>Total</p><p class='nilaiData-3'>{total_angka}</p><p class='namaKota'>Payment</p>"    
        st.markdown(output_total, unsafe_allow_html=True)  


    payment_type_dist = df['payment_type'].value_counts()
    payment_type_dist = payment_type_dist.reset_index()
    payment_type_dist.columns = ['payment_type', 'Count']

    with st.container():
        values = st.slider(
            label='Select a range of values',
            min_value=0,
            max_value=5,
            value=5
        )

        # st.write('Values:', values)
        # st.write(payment_type_dist)
        payment_type_dist = payment_type_dist.head(values)
        fig = px.pie(payment_type_dist, values='Count', names='payment_type')
        st.write(fig)
        
    with st.expander("Penjelasan Tipe Pembayaran") :
        st.write('Dilihat dari grafik diatas, terlihat bahwa metode pembayaran yang sering digunakan oleh pelanggan yaitu menggunakan Credit Card dengan jumlah pengguna mencapai 76,795 pengguna dibandingkan dengan menggunakan metode yang lainnya seperti : Boleto (19,784 pengguna), Voucher (5,775 pengguna) dan Debit Card (1,529 pengguna)') 

elif option == opt4:
    st.subheader('Data rating produk di berbagai kategori')
    st.divider()

    with st.container():
        values = st.number_input("Masukkan Jumlah Kategori Terlaris ", value= 10, min_value=0, max_value=15, step=1)

        ##########################
        produk_terjual_sorted = produk_terjual.sort_values(ascending=True).tail(values)
        # Ubah data menjadi format yang sesuai dengan Altair
        produk_terjual_sorted = produk_terjual_sorted.reset_index()
        produk_terjual_sorted.columns = ['index', 'value']
        produk_terjual_sorted['variable'] = f"{values} Kategori Terlaris"
        ##########################

        # Buat chart menggunakan Altair
        chart = (
            alt.Chart(produk_terjual_sorted)
            .mark_bar(color='skyblue')
            .encode(
                x=alt.X("value", type="quantitative", title="JUMLAH PRODUK TERJUAL"),
                y=alt.Y("index", type="nominal", title="NAMA KATEGORI"),
                color=alt.Color("variable", type="nominal", title=""),
                order=alt.Order("variable", sort="descending")
            )
        )

        # Tampilkan chart menggunakan Streamlit
        st.altair_chart(chart, use_container_width=True)
    
    
    with st.expander("Penjelasan Review Score"):
        st.write('Berdasarkan hasil analisis data pada skala review score, dapat disimpulkan:')
        st.write ('Dominasi Review Score Tinggi: Sebagian besar review memiliki skor tinggi, dengan 57,328 review (sekitar 57%) memberikan nilai 5. Hal ini menunjukkan mayoritas pelanggan cenderung memberikan feedback positif terhadap produk atau layanan.')
        st.write ('Distribusi Review yang Bervariasi: Meskipun skor 5 mendominasi, terdapat variasi dalam distribusi review dengan skor yang lebih rendah. Sebanyak 19,142 review (sekitar 19%) memiliki skor 4, 8,179 review (sekitar 8%) memiliki skor 3, 3,151 review (sekitar 3%) memiliki skor 2, dan 11,424 review (sekitar 11%) memiliki skor 1. Ini menunjukkan adanya variasi dalam pengalaman pelanggan, termasuk beberapa pengalaman yang mungkin kurang memuaskan.')
        st.write ('Perlu Perhatian pada Review Skor Rendah: Meskipun mayoritas review adalah positif, adanya jumlah yang signifikan pada skor 1, 2, dan 3 menunjukkan adanya area yang mungkin perlu perhatian lebih lanjut. Melakukan analisis lebih mendalam terhadap review dengan skor rendah dapat membantu mengidentifikasi masalah atau kekurangan dalam produk atau layanan.')
        st.write ('Rekomendasi untuk Peningkatan Kualitas: Fokus pada area yang menerima skor rendah dapat membantu meningkatkan kualitas produk atau layanan. Mendengarkan umpan balik pelanggan dan mengambil tindakan perbaikan dapat membantu meningkatkan kepuasan pelanggan secara keseluruhan.')
        st.write ('Kesimpulan Umum: Secara keseluruhan, perusahaan atau penyedia layanan dapat merasa lega dengan dominasi review score tinggi, tetapi juga penting untuk tidak mengabaikan review dengan skor rendah. Menganalisis dan mengambil tindakan terhadap masalah yang diidentifikasi dapat meningkatkan kepercayaan pelanggan dan kualitas produk atau layanan secara keseluruhan.seluruhan.')
            
import folium
from streamlit_folium import folium_static
st.subheader('Data kategori produk terlaris')
st.header('Sebaran lokasi Penjual')
st.divider()

# Gabungkan dataset berdasarkan kolom zip code prefix
merged_df = pd.merge(df_sellers, geolocation_df, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

# Hitung jumlah penjual per kota
city_sellers_count = merged_df['seller_city'].value_counts().reset_index()
city_sellers_count.columns = ['City', 'Number of Sellers']

# Mendapatkan latitude dan longitude rata-rata untuk setiap kota
city_coordinates = merged_df.groupby('seller_city')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()

# Membuat peta menggunakan Folium
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=5)  # Koordinat Brazil sebagai pusat peta

# Menambahkan marker untuk setiap kota dengan jumlah penjual terbanyak
for idx, row in city_sellers_count.iterrows():
        city = row['City']
        sellers_count = row['Number of Sellers']
        city_info = city_coordinates[city_coordinates['seller_city'] == city].iloc[0]
        lat = city_info['geolocation_lat']
        lng = city_info['geolocation_lng']
        folium.Marker(location=[lat, lng], popup=f'{city}: {sellers_count} sellers').add_to(m)
    # Menampilkan peta menggunakan Streamlit
folium_static(m)

with st.expander("Penjelasan Selengkapnya"):
    # Kota dengan Penjualan Terbanyak:
    st.subheader('3 Kota dengan Penjualan Terbanyak:')
    st.write('- Sao Paulo: 694 penjual')
    st.write('- Curitiba: 127 penjual')
    st.write('- Rio de Janeiro: 96 penjual')

    # Analisis
    st.subheader('Analisis:')
    st.write('- Sao Paulo adalah kota dengan jumlah penjual terbanyak di antara kota-kota yang terdaftar. Ini menunjukkan bahwa Sao Paulo adalah pusat perdagangan yang penting dalam ekosistem penjualan di Brasil.')
    st.write('- Terdapat konsentrasi penjual yang signifikan di wilayah metropolitan, terutama di Sao Paulo, Rio de Janeiro, dan Curitiba, yang menunjukkan adanya kegiatan ekonomi yang kuat di daerah ini.')
    st.write('- Secara umum, wilayah tenggara Brasil, terutama wilayah metropolitan Sao Paulo, tampak menjadi pusat kegiatan perdagangan dan penjualan.')

    st.write('Dengan demikian, dapat disimpulkan bahwa kota-kota seperti Sao Paulo, Rio de Janeiro, dan Curitiba, khususnya di wilayah tenggara Brasil, memiliki konsentrasi penjual yang signifikan dan merupakan pusat-pusat perdagangan penting di negara tersebut.')




# st.subheader("Region wise Sales")
# # Replace 'customer_city' and 'Sales' with your actual DataFrame columns
# fig = px.pie(df, values="customer_city", names="customer_city", hole=0.5)
# fig.update_traces(text=df["customer_city"], textposition="outside")
# st.plotly_chart(fig, use_container_width=True)












# city = df['customer_city'].value_counts().head(20)
# labels = city.index     
# plt.pie(
#     city, 
#     labels = labels,
#     autopct = '%1.1f%%',
#     explode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
#     startangle = 60,
#     shadow = True
# )
# plt.title('Customer City')
# plt.show()
    
