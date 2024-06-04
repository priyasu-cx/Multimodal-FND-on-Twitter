import streamlit as st
from streamlit_elements import elements, mui, html
from streamlit_elements import nivo
import pandas as pd
from app import reset

def pie_chart_values(fnd_report, url_report, image_report):
    # Define the weights for each report
    fnd_weight = 1.5
    url_weight = 1
    image_weight = 1.2

    # Normalize the weights
    total_weight = fnd_weight + url_weight + image_weight
    fnd_weight /= total_weight
    url_weight /= total_weight
    image_weight /= total_weight

    # Calculate the scores
    fnd_score = fnd_report * fnd_weight * 100
    url_score = url_report * url_weight * 100
    image_score = image_report * image_weight * 100

    return [float(fnd_score), float(url_score), float(image_score)]

def calculate_score(fnd_report, url_report, image_report):
    # Weights for each report (assuming equal weight)
    weight = 10 / 3  # Approximately 3.33

    # Calculate the raw score
    raw_score = (fnd_report + url_report + image_report) * weight

    # Ensure the score is out of 10
    rating = min(raw_score, 10)

    rating = 10 - rating
    
    return float(rating)

def report():
    st.set_page_config(initial_sidebar_state="collapsed", layout="wide", page_title="Tweet Report", page_icon="📄")
    st.title("Tweet Report")
    st.divider()
    
    # Load the data
    tweet = st.session_state.tweet
    uploaded_image = st.session_state.image_uploaded

    fnd_report = st.session_state.fnd_report
    url_report = st.session_state.url_report
    semantics_report = st.session_state.semantics_report
    image_report = st.session_state.image_report
    #--------------------------------------------------------------------------------------------------------------------------------

    # Testing data
    # tweet = "🌟 Prosperity isn't just about financial success; it's the abundance of joy, love, and fulfillment in every aspect of life. When gratitude becomes your default state, abundance follows. Here's to a life rich in experiences, growth, and meaningful connections! ✨ #Prosperity #Abundance #Gratitude"
    # uploaded_image = st.session_state.image_uploaded

    # fnd_report = 1
    # url_report = 1
    # semantics_report = "Misinformation"
    # image_report = 1

    #--------------------------------------------------------------------------------------------------------------------------------

    # Calculate the score
    score = calculate_score(fnd_report, url_report, image_report)

    pie = pie_chart_values(fnd_report, url_report, image_report)

    # print("Report Scores: ", fnd_report, url_report, image_report)
    # print(pie)

    # Columns for other features
    main_col1, main_col2 = st.columns([2,1], gap="medium")

    with main_col2:

        # Make a container
        with st.container(border=True):
            P2_col1, P2_col2 = st.columns([1,8])

            with P2_col1:
                #Insert image in a circle
                st.image("https://i.vgy.me/ghcFZ5.png")

            with P2_col2:
                st.markdown("""
                            <style>
                            .User {
                                font-size: 16px;
                                font-weight: bold;
                            }
                            .username {
                                font-size: 14px;
                                color: grey;
                            }
                            .flex {
                                display: flex;
                                align-items: baseline;
                            }
                            </style>
                            <div class=flex><p class=User>TweetBot&nbsp&nbsp</p><p class=username>&nbsp@iambot &#x2022; Jun 5</p></div>
                            """, unsafe_allow_html=True)

                
                st.write(tweet)
                st.write("<br>", unsafe_allow_html=True)

                image_uploaded = st.session_state.image_uploaded

                if image_uploaded:
                    st.image(uploaded_image, use_column_width=True)

    with main_col1:
        

        if fnd_report == 0 and url_report == 0 and image_report == 0:
            with st.container(border=True):
                if score < 10: st.write("<center class=result-fake>Fake News</center>", unsafe_allow_html=True)
                else: st.write("<center class=result-real>Real News</center>", unsafe_allow_html=True)
                st.write(f'<center class="rating">{score:.2f}/10</center>', unsafe_allow_html=True)
                st.write("<center class=caption>Quality of Info/ Source</center>", unsafe_allow_html=True)
                st.divider()

                st.write("<center class=type>🔍 The tweet is classified as <br><b>Real News</b></center><br>", unsafe_allow_html=True)

                st.write("<center>👍 &ldquo; Truth is like the sun. You can shut it out for a time, but it ain't goin' away.&ldquo; - Elvis Presley</center><br><br>", unsafe_allow_html=True)
        else:
            tc1, tc2 = st.columns([1,2])

            

            with tc1:
                with st.container(border=True):
                    if score < 10: st.write("<center class=result-fake>Fake News</center>", unsafe_allow_html=True)
                    else: st.write("<center class=result-real>Real News</center>", unsafe_allow_html=True)
                    st.write(f'<center class="rating">{score:.2f}/10</center>', unsafe_allow_html=True)
                    st.write("<center class=caption>Quality of Info/ Source</center>", unsafe_allow_html=True)
                    st.divider()

                    st.write(f"<center class=type>The Fake Content has been classified as <br><b>{semantics_report}</b></center><br><br>", unsafe_allow_html=True)


            with tc2:

                with elements("nivo_pie_chart"):

                    DATA = [
                    { "id": "URL", "label": "URL", "value": round(pie[1],2), "color": "hsl(309, 70%, 50%)" },
                    { "id": "Tweet Body", "label": "Tweet Body", "value": round(pie[0],2), "color": "hsl(229, 70%, 50%)" },
                    { "id": "Image", "label": "Image", "value": round(pie[2],2), "color": "hsl(78, 70%, 50%)" },
                    # { "id": "scala", "label": "scala", "value": 254, "color": "hsl(278, 70%, 50%)" },
                    # { "id": "stylus", "label": "stylus", "value": 598, "color": "hsl(273, 70%, 50%)" }
                    ]

                    with mui.Box(sx={"height": 400}):
                        nivo.Pie(
                            data=DATA,
                            margin={"top": 50, "right": 100, "bottom": 100, "left": 100},
                            innerRadius=0.5,
                            padAngle=0.7,
                            cornerRadius=3,
                            activeOuterRadiusOffset=8,
                            borderWidth=1,
                            borderColor={"from": "color", "modifiers": [["darker", 0.8]]},
                            arcLinkLabelsSkipAngle=10,
                            arcLinkLabelsTextColor="grey",
                            arcLinkLabelsThickness=2,
                            arcLinkLabelsColor={"from": "color"},
                            arcLabelsSkipAngle=10,
                            arcLabelsTextColor={"from": "color", "modifiers": [["darker", 4]]},
                            defs=[
                                {
                                    "id": "dots",
                                    "type": "patternDots",
                                    "background": "inherit",
                                    "color": "rgba(255, 255, 255, 0.3)",
                                    "size": 4,
                                    "padding": 1,
                                    "stagger": True,
                                },
                                {
                                    "id": "lines",
                                    "type": "patternLines",
                                    "background": "inherit",
                                    "color": "rgba(255, 255, 255, 0.3)",
                                    "rotation": -45,
                                    "lineWidth": 6,
                                    "spacing": 10,
                                },
                            ],
                            fill=[
                                {"match": {"id": "URL"}, "id": "dots"},
                                {"match": {"id": "Tweet Body"}, "id": "lines"},
                                {"match": {"id": "Image"}, "id": "dots"},
                                # {"match": {"id": "css"}, "id": "dots"},
                                # {"match": {"id": "stylus"}, "id": "lines"},
                            ],
                            legends=[
                                {
                                    "anchor": "bottom",
                                    "direction": "row",
                                    "justify": False,
                                    "translateX": 0,
                                    "translateY": 56,
                                    "itemsSpacing": 0,
                                    "itemWidth": 100,
                                    "itemHeight": 18,
                                    "itemTextColor": "#999",
                                    "itemDirection": "left-to-right",
                                    "itemOpacity": 1,
                                    "symbolSize": 18,
                                    "symbolShape": "circle",
                                    "effects": [
                                        {"on": "hover", "style": {"itemTextColor": "#000"}}
                                    ],
                                }
                            ],
                            theme = {
                                "tooltip": {
                                    "container": {
                                        "background": "#333"
                                    }
                                }
                            }
                        )
        st.markdown(
                """
                <style>
                    .result-fake {
                        font-size: 24px;
                        font-weight: bold;
                        color: red;
                    }
                    .result-real {
                        font-size: 24px;
                        font-weight: bold;
                        color: green;
                    }
                    .rating {
                        font-size: 20px;
                        color: grey;
                    }
                    .caption {
                        font-size: 16px;
                        color: grey;
                    }
                    .type {
                        font-size: 18px;
                    }
                </style>
                """, unsafe_allow_html=True
            )
    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
        
    </style>
    """,
        unsafe_allow_html=True,
    )

    if st.button("Return to Home"):
        st.switch_page("app.py")
        reset()




if __name__ == "__main__":
    report()