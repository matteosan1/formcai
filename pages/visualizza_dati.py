import streamlit as st
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=60)

# Funzione fittizia per simulare la lettura da Google Sheets
# Qui userai la tua logica (es. st.connection o gspread)
def get_data_from_sheets():
    # Esempio di struttura dati che dovresti avere
    data = [
        {"id": 1, "Nome": "Progetto A", "Tipo": "Immagine", "URL": "https://res.cloudinary.com/demo/image/upload/sample.jpg", "Data": "2024-05-20"},
        {"id": 2, "Nome": "Report Tecnico", "Tipo": "PDF", "URL": "https://res.cloudinary.com/demo/image/upload/multi_page_pdf.pdf", "Data": "2024-05-21"}
    ]
    return pd.DataFrame(data)

st.title("🗂️ Archivio Database")

df = get_data_from_sheets()

# Configurazione della tabella per la selezione
st.write("Seleziona una riga per vedere i dettagli:")
event = st.dataframe(
    df, 
    on_select="rerun", 
    selection_mode="single_row",
    hide_index=True,
    use_container_width=True
)

# Controllo se l'utente ha selezionato qualcosa
if len(event.selection.rows) > 0:
    row_index = event.selection.rows[0]
    row_data = df.iloc[row_index]
    
    st.divider()
    
    # Layout a due colonne per i dettagli
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Dettagli Riga")
        st.write(f"**Nome:** {row_data['Nome']}")
        st.write(f"**Tipo:** {row_data['Tipo']}")
        st.write(f"**Data:** {row_data['Data']}")
        st.caption(f"ID Record: {row_data['id']}")

    with col2:
        st.subheader("Anteprima Documento")
        url = row_data['URL']
        
        if row_data['Tipo'].lower() == "immagine" or url.endswith(('.jpg', '.jpeg', '.png')):
            # TRUCCO CLOUDINARY: Aggiungiamo parametri all'URL per rimpicciolire l'anteprima al volo
            # Inseriamo 'w_400,c_limit' nell'URL per non scaricare l'immagine originale gigante
            thumb_url = url.replace("/upload/", "/upload/w_400,c_limit/")
            st.image(thumb_url, caption="Anteprima (ottimizzata da Cloudinary)")
            
        elif row_data['Tipo'].lower() == "pdf" or url.endswith('.pdf'):
            # Per i PDF, Cloudinary può generare un'anteprima della prima pagina come immagine!
            # Basta cambiare l'estensione finale da .pdf a .jpg
            pdf_thumb = url.replace(".pdf", ".jpg").replace("/upload/", "/upload/w_400,c_limit,pg_1/")
            st.image(pdf_thumb, caption="Anteprima prima pagina PDF")
            st.link_button("Apri PDF Completo", url)

else:
    st.info("💡 Clicca sul quadratino a sinistra di una riga per visualizzare i dettagli e l'anteprima.")