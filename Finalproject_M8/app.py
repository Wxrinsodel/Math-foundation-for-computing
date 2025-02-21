import numpy as np
import plotly.graph_objects as go
import math
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

#เบสิเอ้อ
def create_bezier_surface():
    # Control Points >> array is used to create an array
    x = np.array([[-0.5, -2, 0], [1, 1, 1], [2, 2, 2]])
    y = np.array([[2, 1, 0], [2, 0, -1], [2, 1, 1]])
    z = np.array([[1, 0, 2], [0, -0.5, 2], [0.5, 1, 2]])

    # Number of Cells for each Direction
    uCELLS = 50  # Increased for smoother surface
    wCELLS = 50  # Increased for smoother surface

    # Dependent variable >> shape is used to get the dimensions of the array
    uPTS = x.shape[0]
    wPTS = x.shape[1]

    # Total number of subdivisions
    n = uPTS - 1
    m = wPTS - 1

    # Parametric Variables >> linspace creates an array of evenly spaced values
    u = np.linspace(0, 1, uCELLS)
    w = np.linspace(0, 1, wCELLS)

    # Initialized Empty Matrices >> zeros creates an array of zeros
    xBezier = np.zeros((uCELLS, wCELLS))
    yBezier = np.zeros((uCELLS, wCELLS))
    zBezier = np.zeros((uCELLS, wCELLS))

    # Binomial Coefficients >> determines the weight of each control point and helps compute Bezier surfaces correctly.
    def Ni(n, i):
        return math.factorial(n) / (math.factorial(i) * math.factorial(n - i))


    def Mj(m, j):
        return math.factorial(m) / (math.factorial(j) * math.factorial(m - j))


    # Bernstein Basis Polynomial >> used to blend control points smoothly
    def J(n, i, u):
        return np.array([Ni(n, i) * (u_val ** i) * (1 - u_val) ** (n - i) for u_val in u])


    def K(m, j, w):
        return np.array([Mj(m, j) * (w_val ** j) * (1 - w_val) ** (m - j) for w_val in w])

    # Main loop
    for i in range(uPTS): 
        for j in range(wPTS): 
            Jt = J(n, i, u).reshape(-1, 1) #resharp is used to change the shape of an array
            Kt = K(m, j, w).reshape(1, -1)

            xBezier += Jt @ Kt * x[i, j] # @ is used for matrix multiplication
            yBezier += Jt @ Kt * y[i, j] 
            zBezier += Jt @ Kt * z[i, j]

    # Create figure
    fig = go.Figure()

    # Add surface plot >> fig.add_trace is used to add a trace to the figure
    fig.add_trace(go.Surface(
        x=xBezier,
        y=yBezier,
        z=zBezier,
        colorscale='viridis',
        opacity=0.8,
        name='Bezier Surface',
        showscale=False
    ))

    # Add control points
    fig.add_trace(go.Scatter3d(
        x=x.flatten(), #flatten is used to return a copy of the array collapsed into one dimension
        y=y.flatten(),
        z=z.flatten(),
        mode='markers', #mode is used to set the trace type and markers is used to create a scatter plot
        marker=dict(
            size=8,
            color='red',
            symbol='circle'
        ),
        name='Control Points'
    ))

    # Update layout with more detailed configuration
    fig.update_layout(
        title={
            'text': 'Interactive Bezier Surface',
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        scene={
            'xaxis_title': 'X Axis',
            'yaxis_title': 'Y Axis',
            'zaxis_title': 'Z Axis',
            'camera': dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            ),
            'aspectmode': 'cube'
        },
        width=800,
        height=800,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig.to_html(full_html=False, include_plotlyjs=True)


@app.route('/')
def index():
    plot_html = create_bezier_surface()
    return render_template('index.html', plot_html=plot_html)

@app.route('/static/<path:filename>') 
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=21002, debug=True)