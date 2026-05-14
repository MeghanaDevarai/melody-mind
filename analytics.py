import pandas as pd
import plotly.express as px


def show_graph(emotions):

    df = pd.DataFrame({
        'Emotion': emotions
    })

    fig = px.histogram(
        df,
        x='Emotion',
        title='Emotion Analytics'
    )

    return fig