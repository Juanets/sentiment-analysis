import plotly.plotly as py  
import plotly.tools as tls   
import plotly.graph_objs as go
from secrets import *

tls.set_credentials_file(
	username=username, 
	api_key=api_key, 
	stream_ids=stream_ids
)

class Plot(object):

    def __init__(self):
        stream_tokens = tls.get_credentials_file()['stream_ids']
        self.token = stream_tokens[0]
        self.stream = go.Stream(token=self.token)
        self.s = py.Stream(self.token)

    def init_plot(self, topic):
        bar1 = go.Bar(
            x=[topic],
            y=[0],
            xaxis='x2',
            yaxis='y2',
            marker=dict(color="red"),
            name='Twitter Sentiment Analysis',
            stream=self.stream
        )

        data = go.Data([bar1])

        layout = go.Layout(
            yaxis2=dict(
                range=[-1, 1],
            )
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename='sentiment-analysis')