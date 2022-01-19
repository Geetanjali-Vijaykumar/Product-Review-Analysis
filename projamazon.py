import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import joblib


pipe_lr = joblib.load(open("model_amazon_review.pkl", "rb"))



def predict_emotions(docx):
    results = pipe_lr.predict([docx])
    return results[0]

def get_prediction_proba(docx):
    results = pipe_lr.predict_proba([docx])
    return results

emotions_emoji_dict = {"Neutral":"😐","Positive":"🙂","Negative":"☹️"}


def main():
    st.set_page_config(layout = "wide")
    st.markdown("""
        <style>
            body {
                    background: #ff0099; 
                                }
        </style>
    """, unsafe_allow_html=True) 
    st.title("Welcome to Sentiment Analysis for the Product Reviews")
    st.header("Classify if the review is Positive, Negative or Neutral!!!!")
    raw_text = st.text_area('Type Here:')
    submit_text = st.button("Predict")




    if submit_text:
        col1,col2 = st.columns(2)

        prediction = predict_emotions(raw_text)
        probability = get_prediction_proba(raw_text)
                
        with col1:
            #st.success("hello")
            st.success("Prediction")
            emoji_icon = emotions_emoji_dict[prediction]
            st.write("{}:{}".format(prediction,emoji_icon))
            st.write("Confidence: {}".format(np.max(probability)))

        with col2:
            #st.success(raw_text)
            st.success("Prediction Probability")
            #st.write(probability)
            proba_df = pd.DataFrame(probability,columns=pipe_lr.classes_)
            st.write(proba_df.T)
            proba_df_clean = proba_df.T.reset_index()
            proba_df_clean.columns = ["Sentiment","probability"]
    
            fig = alt.Chart(proba_df_clean).mark_bar().encode(x='Sentiment',y='probability',color='Sentiment')
            st.altair_chart(fig,use_container_width=True)


       
    


if __name__=='__main__':
    main()
