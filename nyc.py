import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Función para leer los registros, con cache para mejorar el rendimiento
@st.cache
def cargar_datos(archivo, n_registros=500):
    # Lee los primeros n registros de un archivo CSV
    df = pd.read_csv(archivo)
    return df.head(n_registros)

# Cargar datos
archivo = './citibike-tripdata.csv'  # Ruta del archivo CSV
df = cargar_datos(archivo)

# Renombrar columnas
df.rename(columns={'start_lat': 'lat', 'start_lng': 'lon'}, inplace=True)

# Sidebar
st.sidebar.title("Opciones del Dashboard")


st.sidebar.write("Matricula: zs21004524.")
st.sidebar.write("zs21004524@estudiantes.uv.mx")

st.sidebar.image("https://firebasestorage.googleapis.com/v0/b/paradigmas-luigi196362.appspot.com/o/javascript%2Fimages%2Fcredencial.jpg?alt=media&token=ffba3513-0c65-4540-8bdf-140a9ba8f468")


row_data = st.sidebar.checkbox("Show row data", value=False)

if row_data:
    st.subheader("Raw Data")
    st.write(df)

tours_hour = st.sidebar.checkbox("Recorridos por hora", value=False)


# Gráfica de barras de recorridos por hora
df['hora'] = pd.to_datetime(df['started_at']).dt.hour
recorridos_por_hora = df.groupby('hora').size()

st.sidebar.subheader("Gráfica de recorridos por hora")
fig, ax = plt.subplots()
ax.bar(recorridos_por_hora.index, recorridos_por_hora.values)
ax.set_xlabel('Hora')
ax.set_ylabel('Número de recorridos')
ax.set_title('Recorridos por hora')

if tours_hour:
    st.subheader("Recorridos por hora")
    st.pyplot(fig)


# Control slider para seleccionar la hora del día
hora_seleccionada = st.sidebar.slider('Selecciona la hora del día', 0, 23, 12)

# Filtrar por la hora seleccionada
df_filtrado = df[df['hora'] == hora_seleccionada]

# Visualizar el mapa con los puntos GPS
st.sidebar.subheader(f"Estaciones con recorridos a las {hora_seleccionada}:00")
st.map(df_filtrado[['lat', 'lon']])

