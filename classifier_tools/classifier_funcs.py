import streamlit as st
import numpy as np
from PIL import Image
from numpy import asarray
import pandas as pd


def create_predictions_df(predictions, images):
    labeled_predictions = list(map(lambda x: "good "if x >= 0.5 else "bad", predictions))
    # If no predictions have been done before add all the image predictions to the dataframe
    if st.session_state.pred_df.empty:
        for i, img in enumerate(images):
            row = {"Filename": img.name, 'Sorted': labeled_predictions[i], 'Probability': predictions[i]}
            st.session_state.pred_df = pd.concat(
                [st.session_state.pred_df, pd.DataFrame.from_records([row])], ignore_index=True)
    # If predictions have been done before only add new entries and modify old entries if the prediction changed
    else:
        for i, img in enumerate(images):
            existing_entry = st.session_state.pred_df.loc[st.session_state.pred_df["Filename"] == img.name, "Sorted"]
            if existing_entry.empty == False:  # There is an existing prediction for this image
                old_label = existing_entry.to_string(index=False)
                if old_label != labeled_predictions[i]:
                    row = [img.name, labeled_predictions[i], predictions[i]]
                    st.session_state.pred_df.loc[st.session_state.pred_df["Filename"] == img.name] = row
            else:  # No entry exists for this image name
                row = {"Filename": img.name, 'Sorted': labeled_predictions[i], 'Probability': predictions[i]}
                st.session_state.pred_df = pd.concat(
                    [st.session_state.pred_df, pd.DataFrame.from_records([row])], ignore_index=True)


def create_prediction_ready_data(images_list: list, img_shape: tuple):
    """returns a numpy array of the shape (number_images,img_shape,3)"""
    images = []
    for image in images_list:
        img = Image.open(image)
        img_array = pre_process_img(img, img_shape)
        images.append(img_array)
    data = np.vstack(images)
    return data


def pre_process_img(image, img_shape: tuple) -> list:
    """returns np.array resized to (1,img_shape,3)"""
    img = image.resize(img_shape, Image.ANTIALIAS)
    imgArray = asarray(img)
    imgArray = imgArray.reshape((1,) + img_shape + (3,))  # Create batch axis
    return imgArray


def show_curr_image_classifier(images_list):
    # Display a the done image when the all images have been displayed
    if st.session_state.img_idx >= len(images_list):
        image = Image.open("./assets/done.jpg")
        st.image(image, width=300)
    elif images_list == []:
        image = Image.open("./assets/new_loading_sniffer.jpg")
    else:
        st.write("Index", st.session_state.img_idx)
        if not st.session_state.pred_df.empty:
            curr_pred = st.session_state.pred_df[st.session_state.pred_df["Filename"]
                                                 == images_list[st.session_state.img_idx].name]
            st.write("Predicted as ", curr_pred["Sorted"].iloc[0], "with ", curr_pred["Probability"].iloc[0])
        # caption is "" when images_list is empty otherwise its image name
        caption = '' if images_list == [
        ] else f'#{st.session_state.img_idx} {images_list[st.session_state.img_idx].name}'
        image = Image.open(images_list[st.session_state.img_idx])
        st.image(image, caption=caption, width=300)


def view_prediction_images(images_list):
    if not st.session_state.pred_df.empty:
        images_per_row = st.slider("The number of images per row", step=1, value=4, min_value=1, max_value=8)
        n_rows = len(images_list) / images_per_row
        n_rows = int(np.ceil(n_rows))  # round up because range is end exclusive
        for row_num in range(n_rows):
            cols = st.columns(images_per_row)
            start = row_num * images_per_row
            end = start + images_per_row
            if end > len(images_list):
                end = len(images_list)
            for col, image in zip(cols, images_list[start:end]):
                curr_pred = st.session_state.pred_df[st.session_state.pred_df["Filename"] == image.name]
                predicted_label = curr_pred["Sorted"].iloc[0]
                col.image(image, use_column_width=True, caption=f"{predicted_label}")
