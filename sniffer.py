import streamlit as st
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from PIL import Image
from datetime import datetime
from classifier_tools import classifier_funcs

st.set_page_config(
     page_title="Sniffer",
     page_icon="🐕",
     layout="centered",
     initial_sidebar_state="collapsed",
     menu_items={
         'Get Help': None,
         'Report a bug': None,
         'About': "# Sniffer. Sort your *extremely* cool images!"
     }
 )

# Load the tensorflow model only once
@st.experimental_singleton
def get_model(model_name:str,model_path:str=os.getcwd()+ os.sep+"models"):
    model_path+=os.sep+model_name
    model = tf.keras.models.load_model(model_path+os.sep+"model")
    return model

# Load the model from the singleton cache
model=get_model("binary_classification_model_v_2_1")

with st.expander("See Upload", expanded=True):
    uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
    images_list=uploaded_files


def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return csv_filename

# Initialize Sniffer's states
if 'img_idx' not in st.session_state:
    st.session_state.img_idx=0
if 'choice_df' not in st.session_state:
    st.session_state.choice_df=pd.DataFrame(columns=['Filename','Sorted'])
if 'pred_df' not in st.session_state:
    st.session_state.pred_df=pd.DataFrame(columns=['Filename','Sorted','Probability'])

# img_idx will always be inside images_list
if st.session_state.img_idx > (len(images_list)+2):
    st.session_state.img_idx = (len(images_list)-1) if (len(images_list)-1)>0 else 0

def create_csv(df,df2=None):
    if  not isinstance(df2,type(None)):
        if df2.empty == False and df.empty == False:
            return pd.concat([df,df2],ignore_index=True).to_csv(index=False).encode('utf-8')
        elif df2.empty == False and df.empty == True:
            return df2.to_csv(index=False).encode('utf-8')
    return df.to_csv(index=False).encode('utf-8')


def predict():
    # Make sure the images list is not empty and the index is valid
    if images_list != [] and st.session_state.img_idx <= len(images_list)-1:
        start =0 if st.session_state.img_idx <= 0 else st.session_state.img_idx
        end=len(images_list)-1
        img_shape=(100,100)
        if start <= end:
            data=classifier_funcs.create_prediction_ready_data(images_list[start:end+1],img_shape)
            predictions=model.predict(data)
            predictions=predictions.flatten().tolist()
            classifier_funcs.create_predictions_df(predictions,images_list[start:end+1])


def yes_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1)   :
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"good"}
        st.session_state.choice_df=pd.concat([st.session_state.choice_df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx ==(len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx} /{ len(images_list)} ')


def no_button():
    if -1 < st.session_state.img_idx <= (len(images_list)-1) :
        row={"Filename":images_list[st.session_state.img_idx].name,'Sorted':"bad"}
        st.session_state.choice_df=pd.concat([st.session_state.choice_df,pd.DataFrame.from_records([row])],ignore_index=True)
        st.session_state.img_idx += 1
    elif st.session_state.img_idx == (len(images_list)):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort { st.session_state.img_idx}/{ len(images_list)}')


def undo_button():
    if st.session_state.img_idx >0:
        st.session_state.img_idx -= 1
        if images_list != [] and st.session_state.img_idx <= (len(images_list)-1) :
            drop_filename=images_list[st.session_state.img_idx].name
            index=st.session_state.choice_df.loc[st.session_state.choice_df['Filename'] == drop_filename].index.values
            st.session_state.choice_df.drop(index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')


if images_list==[]:
    image= Image.open("./assets/new_loading_sniffer.jpg")
else:
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
    else:
        image = Image.open(images_list[st.session_state.img_idx])

st.title("Sniffer🐕")
st.image("./assets/sniffer.jpg")

# Sets num_image=1 if images_list is empty
num_images=(len(images_list)) if (len(images_list))>0 else 1

try:
    my_bar = st.progress((st.session_state.img_idx)/num_images)
except st.StreamlitAPIException:
    my_bar = st.progress(0)


col1,col2,col3,col4=st.columns(4)
with col1:
    st.button(label="Yes",key="yes_button",on_click=yes_button)
    st.button(label="No",key="no_button",on_click=no_button)
    st.button(label="Undo",key="undo_button",on_click=undo_button)
    st.button(label="✨ Predict ✨",key="predict_button",on_click=predict)
with col2:
    # Display done.jpg when all images are sorted 
    if st.session_state.img_idx>=len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image,width=300)
    else:
        # caption is "" when images_list is empty otherwise its image name 
        caption = '' if images_list==[] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
        st.image(image, caption=caption,width=300)
    
with col4:
    st.download_button(
     label="Download choices as CSV 🦮", 
     data=create_csv( st.session_state.choice_df),
     file_name= create_csv_name(),
     mime='text/csv',)

    st.download_button(
     label="Download predictions as CSV ✨",
     data=create_csv(st.session_state.pred_df),
     file_name= create_csv_name(),
     mime='text/csv',)

    st.download_button(
     label="Download predictions & choices as CSV 💻",
     data=create_csv(st.session_state.choice_df,st.session_state.pred_df),
     file_name= create_csv_name(),
     mime='text/csv',)

with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.pred_df)
    st.dataframe(st.session_state.choice_df)
    st.bar_chart(st.session_state.choice_df['Sorted'].value_counts())
