from tkinter import image_names
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="Sniffer",
    page_icon="🐕",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': "https://github.com/2320sharon/Streamlit_Sniffer",
        'Report a bug': "https://github.com/2320sharon/Streamlit_Sniffer/issues",
        'About': "# Sniffer. Sort your *extremely* cool images!"
    }
)


def get_percent_blk_pixels(file):
    img = Image.open(file)
    img_array = np.array(img)
    w, h = img_array.shape[0:2]
    total_pixels = w * h if img_array.ndim < 3 else w * h * img_array.shape[2]
    black_count = np.sum(img_array == 0)
    return np.round(black_count / total_pixels, 3)


with st.expander("Upload Images", expanded=True):
    uploaded_files = st.file_uploader("Choose a jpg file", accept_multiple_files=True)
    for uploaded_file in uploaded_files:
        bytes_data = uploaded_file.read()
    images_list = uploaded_files


def create_csv_name(csv_filename: str = None) -> str:
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
    st.session_state.img_idx = 0
if 'undo_indexes' not in st.session_state:
    st.session_state.undo_indexes = [0]
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Filename', 'Sorted'])


if st.session_state.img_idx > (len(images_list) + 2):
    st.session_state.img_idx = (len(images_list) - 1) if (len(images_list) - 1) > 0 else 0


def create_csv():
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    st.session_state.df.to_csv().encode('utf-8')
    return st.session_state.df.to_csv().encode('utf-8')


def increment_index(view_images_box):
    """increments the st.session_state.img_idx to the next valid image index depending on the checkbox
    Args:
        view_images_box (bool): Checkbox to view images with black pixel% > limit is active
    """
    if view_images_box:
        st.session_state.img_idx += 1
    elif not view_images_box:
        # Add the current index as a valid index to list of valid index to undo to
        st.session_state.undo_indexes.append(st.session_state.img_idx)
        if get_percent_blk_pixels(images_list[st.session_state.img_idx]) > blk_percent:
            # Continue incrementing index while in range and percnt_blk_pixels > limit
            while (-1 < st.session_state.img_idx <= (len(images_list) - 1)
                   ) and (get_percent_blk_pixels(images_list[st.session_state.img_idx]) > blk_percent):
                st.session_state.img_idx += 1
        else:
            st.session_state.img_idx += 1


def index_out_of_range(idx, length):
    if idx == (length):
        st.success('All images have been sorted!')
        st.balloons()
    else:
        st.warning(f'No more images to sort {idx} /{length} ')


def yes_button(**kwargs):
    view_images_box = kwargs["checkbox"]
    if -1 < st.session_state.img_idx <= (len(images_list) - 1):
        if get_percent_blk_pixels(images_list[st.session_state.img_idx]) <= blk_percent:
            row = {"Filename": images_list[st.session_state.img_idx].name, 'Sorted': "good"}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame.from_records([row])], ignore_index=True)
        increment_index(view_images_box)
    else:
        # Handles all cases when index is out of range
        index_out_of_range(st.session_state.img_idx, len(images_list))


def no_button(**kwargs):
    view_images_box = kwargs["checkbox"]
    if -1 < st.session_state.img_idx <= (len(images_list) - 1):
        if get_percent_blk_pixels(images_list[st.session_state.img_idx]) <= blk_percent:
            row = {"Filename": images_list[st.session_state.img_idx].name, 'Sorted': "bad"}
            st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame.from_records([row])], ignore_index=True)
        increment_index(view_images_box)
    else:
        # Handles all cases when index is out of range
        index_out_of_range(st.session_state.img_idx, len(images_list))


def undo_button(**kwargs):
    view_images_box = kwargs["checkbox"]
    if view_images_box:
        st.session_state.img_idx -= 1
    elif not view_images_box:
        st.session_state.img_idx = st.session_state.undo_indexes.pop()
        # Ensure the list of available undo indexes are never empty
        if len(st.session_state.undo_indexes) == 0:
            st.session_state.undo_indexes.append(0)
    # Remove filename from the dataframe
    if st.session_state.img_idx > 0:
        if images_list != [] and st.session_state.img_idx <= (len(images_list) - 1):
            drop_filename = images_list[st.session_state.img_idx].name
            drop_index = st.session_state.df.loc[st.session_state.df['Filename'] == drop_filename].index.values
            st.session_state.df.drop(drop_index, axis=0, inplace=True)
    else:
        st.warning('Cannot Undo')


st.title("Sniffer🐕")
st.image("./assets/sniffer.jpg")

# Sets num_image=1 if images_list is empty
num_images = (len(images_list)) if (len(images_list)) > 0 else 1

try:
    my_bar = st.progress((st.session_state.img_idx) / num_images)
except st.StreamlitAPIException:
    my_bar = st.progress(0)


col1, col2, col3, col4 = st.columns(4)
with col1:
    blk_percent = st.slider("Percentage of Black Pixels Allowed:", step=0.01, value=0.50, min_value=0.0, max_value=1.0)
    view_images_box = st.checkbox("See Images that exceed percentage of black pixel limit (They won't be sorted)")
    st.button(label="Yes", key="yes_button", on_click=yes_button, kwargs={"checkbox": view_images_box})
    st.button(label="No", key="no_button", on_click=no_button, kwargs={"checkbox": view_images_box})
    st.button(label="Undo", key="undo_button", on_click=undo_button, kwargs={"checkbox": view_images_box})

with col2:
    st.write(f"{st.session_state.img_idx} of {num_images}")
    if images_list == []:
        image = Image.open("./assets/new_loading_sniffer.jpg")
    else:
        # Display done.jpg when all images are sorted
        if st.session_state.img_idx >= len(images_list):
            image = Image.open("./assets/done.jpg")
            st.image(image, width=300)
        else:
            percent_blk_pixels = get_percent_blk_pixels(images_list[st.session_state.img_idx])
            st.write(f"Percentage of Black Pixels : {round(percent_blk_pixels*100,4)}%")
            if percent_blk_pixels > blk_percent:
                st.write("This image exceeds limit of allowed black_pixels. It will not be sorted.")
            if st.session_state.img_idx >= len(images_list):
                image = Image.open("./assets/done.jpg")
                st.image(image, width=300)
            else:
                # caption is "" when images_list is empty otherwise its image name
                image = Image.open(images_list[st.session_state.img_idx])
                caption = '' if images_list == [
                ] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
                st.image(image, caption=caption, width=300)

with col4:
    st.download_button(
        label="Download data as CSV 💻",
        data=create_csv(),
        file_name=create_csv_name(),
        mime='text/csv',
    )

with st.expander("See Dataset Details 📈"):
    st.dataframe(st.session_state.df)
    st.bar_chart(st.session_state.df['Sorted'].value_counts())
