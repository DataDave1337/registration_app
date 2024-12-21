import pandas as pd
import streamlit as st
import os
import datetime


i=0
def iban_on_change():
    global i
    st.write(f'Test {i}')
    i += 1

st.set_page_config(page_title='Aufnahme App', page_icon=':rocket:', layout='wide')
must_haves = [
    'Vorname',
    'Nachname',
    'Geschlecht',
    'Geburtsdatum',
    'Straße',
    'PLZ',
    'Ort',
    'E-Mail_P1',
    'Eintrittsdatum',
    'Kontoinhaber',
    'IBAN',
    'Mandatsreferenz',
]

opt_cols = [
    'Status',
    'Zahlungsart',
    'Mitglieds-Nr',
    'Anrede',
    'Land',
    'Mobil_P1',
    'Telefon_P1',
    'Fax_P1',
    'Telefon_G2',
    'Mobil_G2',
    'Fax_G2',
    'E-Mail_G2',
    'Titel',
    'BIC',
    'Kreditinstitut',
    'Kontonummer',
    'Bankleitzahl',
    'SEPA-Mandatstyp_1',
    'SEPA-Unterschriftsdatum_1',
    'SEPA-Merkmal_1',
    'SEPA-Gültigkeitsdatum_1',
    'SEPA-Benachrichtigungsdatum_1',
    'Austrittsdatum',
    'Abteilung_1',
    'Abteilungseintritt_1',
    'Beitragsbezeichnung_1_1',
    'Beitragsstart_1_1',
    'Gemeinschaft'
]
cols = must_haves + opt_cols
row_dict = {k: '' for k in cols}

st.header('Aufnahme App')

geschlechter = ['männlich', 'weiblich', 'divers']
beitraege = [
    'Jugendliche, Studenten, Schüler, Arbeitslose',
    'Erwachsene',
    'sonstiger ermäßigter Beitrag'
]
with st.form('antrag', clear_on_submit=False):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('##### Persönliches')
        row_dict['Vorname'] = st.text_input('Vorname')
        row_dict['Nachname'] = st.text_input('Nachname')
        row_dict['Geschlecht'] = st.selectbox('Geschlecht', geschlechter)
        row_dict['Geburtsdatum'] = st.text_input('Geburtsdatum')
    with col2:
        st.markdown('##### Wohnort')
        row_dict['Straße'] = st.text_input('Straße und Hausnummer')
        row_dict['PLZ'] = str(st.text_input('Postleitzahl', value='53859'))
        row_dict['Ort'] = st.text_input('Stadt / Ort', value='Niederkassel')
        st.markdown('###')
        st.markdown('##### Kommunikation')
        row_dict['Telefon_P1'] = str(st.text_input('Telefon'))
        row_dict['Mobil_P1'] = str(st.text_input('Mobil'))
        # row_dict['Telefon_P1'] = 'Testvorname'
        row_dict['E-Mail_P1'] = st.text_input('E-Mail')
    with col3:
        st.markdown('##### Beitritt und Zahlungsinformationen')
        beitritt_datum = str(st.text_input('Beitrittsdatum (mit 19xx/20xx!)'))
        row_dict['Beitragsbezeichnung_1_1'] = st.selectbox('Beitrag', beitraege)
        st.markdown('###')
        st.markdown('##### Zahlungsinformationen')
        row_dict['Kontoinhaber'] = st.text_input('Kontoinhaber')
        iban = str(st.text_input('IBAN'))
        row_dict['IBAN'] = iban
        # n = 4
        # iban = " ".join([iban[i:i+n] for i in range(0, len(iban), n)])
        # st.write(iban)
        row_dict['Mandatsreferenz'] = str(st.text_input('Mandatsreferenz'))

    row_dict['Status'] = 'aktiv'
    row_dict['Zahlungsart'] = 'Lastschrift'
    row_dict['Land'] = 'Deutschland'
    row_dict['Eintrittsdatum'] = beitritt_datum

    row_dict['SEPA-Mandatstyp_1'] = 'Folgelastschrift'
    row_dict['SEPA-Unterschriftsdatum_1'] = beitritt_datum
    row_dict['SEPA-Merkmal_1'] = 'wiederkehrend'
    row_dict['Abteilung_1'] = 'Tischtennis'
    row_dict['Abteilungseintritt_1'] = beitritt_datum

    row_dict['Beitragsstart_1_1'] = beitritt_datum
    row_dict['Beitragsbezeichnung_1_2'] = 'Aufnahmegebühr'
    row_dict['Beitragsstart_1_2'] = beitritt_datum

    date_str = datetime.date.today()
    file_path = f'import_{date_str}.csv'
    import_file_exists = os.path.isfile(file_path)
    btn_msg = f'Append to import file {file_path}' if import_file_exists else 'Create import file'
    submitted = st.form_submit_button(btn_msg)

    if submitted:
        df = pd.DataFrame([row_dict])
        must_haves_null = [c for c in must_haves if row_dict[c] == '']
        if len(must_haves_null) > 0:
            st.error(f'{must_haves_null} leer')
        else:
            if import_file_exists:
                # old_df = pd.read_csv(file_path, sep=';', encoding='cp1252')
                old_df = pd.read_csv(file_path, sep=';', encoding='utf-8-sig')
                df = pd.concat([old_df, df]).reset_index(drop=True)
            df.to_csv(file_path, index=False, sep=';', encoding='utf-8-sig')
            # df.to_csv(file_path, index=False, sep=';', encoding='cp1252')
            st.success(f"written {row_dict['Vorname']} {row_dict['Nachname']} to {file_path}")
