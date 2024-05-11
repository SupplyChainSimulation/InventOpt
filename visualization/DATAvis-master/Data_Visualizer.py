import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from sklearn import datasets
import plotly.graph_objects as go
import random

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.neural_network import MLPRegressor

# Author: Neha Karanjkar, IIT Goa
# edited by: Tushar Lone

# This particular version:
# Single value for sliders instead of ranges
# plot3D function is edited, and plotly 3D surface function is used 
# minor modifications to choose input parameters (SR1, sR1, ...) by default

@st.cache
def load_data(file):
    data = pd.read_csv(file)
    return data


@st.cache
def generate_data1(num_rows, num_axes, num_functions):
    X,F_X = datasets.make_regression(n_samples=num_rows, n_features=num_axes, n_informative=min(int(num_axes/2),1), 
            n_targets=num_functions, effective_rank=min(1,int(num_axes/2)), shuffle=True)
    column_names=["X"+str(i+1) for i in range(num_axes)]
    column_names+= ["F"+str(i+1) for i in range(num_functions)]
    data=np.concatenate((X,F_X),axis=1)
    df = pd.DataFrame(data=np.concatenate((X,F_X),axis=1),columns=column_names)
    return df

@st.cache
def compute_function_values(df, num_rows, num_axes, num_functions):
    f_names=r"" 
    for i in range(num_functions):
        # make a random array of coefficients and powers to create each function as a random polynomial
        f_names+="\n - $$f_"+str(i+1)+"="        
        powers = [random.choice([0,1,2,3]) for i in range(num_axes)]
        coeffs = [random.randint(-3,3) for i in range(num_axes)]
        function_column = np.zeros(num_rows)
        for j in range(num_axes):
            function_column += (coeffs[j] * df['x' + str(j + 1)].pow(powers[j]))
            f_names+=str(abs(coeffs[j]))+" x_"+str(j+1)+"^{"+str(powers[j])+"}"
            if j != (num_axes-1):
                f_names+="+" if (coeffs[j+1] >0) else "-"
        f_names+="$$"
        df['f' + str(i + 1)] = function_column
    return df, f_names

@st.cache
def generate_random_data(num_rows, num_axes, num_functions):
    axis_points = np.random.random(size=(num_rows, num_axes))
    df = pd.DataFrame(axis_points, columns=['x' + str(i) for i in range(1, num_axes + 1)])
    return compute_function_values(df, num_rows, num_axes, num_functions)
 
@st.cache
def generate_grid_data(num_pts_per_axes, num_axes, num_functions):
    axis_points = [np.linspace(0, 1, num_pts_per_axes) for _ in range(num_axes)]
    meshgrid = np.meshgrid(*axis_points, indexing='ij')
    meshgrid = np.array(meshgrid).T.reshape(-1, num_axes) 
    df = pd.DataFrame(meshgrid, columns=['x' + str(i) for i in range(1, num_axes + 1)])
    num_rows = (num_pts_per_axes)**num_axes
    return compute_function_values(df, num_rows, num_axes, num_functions)
    

def to_csv(df):
    data_csv = df.to_csv(path_or_buf=None, sep=',', index=False) 
    return data_csv

@st.cache
def slice_data(data, other_axes, values):
    data_slice=data
    for i, axis in enumerate(other_axes):
        #data_slice = data_slice[(data_slice[axis] >= values[i][0]) & (data_slice[axis] <= values[i][1])]
        data_slice = data_slice[data_slice[axis] == values[i]]
    return data_slice

from scipy.interpolate import Rbf

# generate an interpolation from the data using Radial Basis Functions
@st.cache
def interpolate_rbf(df, axis_columns, function_columns):
    rbf_functions=[]
    points = df[axis_columns].to_numpy()
    for function_column in function_columns:
        values = df[function_column].to_numpy()
        rbf_function = Rbf(*points.T, values, function='thin_plate')
        rbf_functions.append(rbf_function)
    return rbf_functions
    
def plot_3d(data_slice, selected_x_axis, selected_y_axis, selected_function):
    #fig = px.scatter_3d(data_slice, x=selected_x_axis, y=selected_y_axis,z=selected_function, color=selected_function, color_continuous_scale=st.session_state.colorscale)
    #fig.update_layout(scene = dict(aspectmode='cube'),template='plotly',
    #    margin={"l":0,"r":0,"t":0,"b":0} 
    #)
    #fig.update_traces(marker_size=st.session_state.marker_size)    
    unique_vals = len(np.unique(data_slice[selected_x_axis].values))
    z=np.array((data_slice[selected_function].values))
    z=np.resize(z,(unique_vals,unique_vals))
    x=np.array((data_slice[selected_x_axis].values))
    x=np.resize(x,(unique_vals,unique_vals))
    y=np.array((data_slice[selected_y_axis].values))
    y=np.resize(y,(unique_vals,unique_vals))
    
    fig = go.Figure(data=[go.Surface(z=z,x=x,y=y)])
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='Slice at given SD,sD', autosize=True)
    return fig

    
@st.cache
def add_interpolation_surface(fig, data, axes, selected_x_axis, selected_y_axis, rbf_func, metamodel_slice_values):
    # to add a surface plot of the meta-model:
    x_axis = data[selected_x_axis].unique()
    y_axis = data[selected_y_axis].unique()
    X, Y = np.meshgrid(x_axis, y_axis)
    x_index = axes.index(selected_x_axis)
    x_index,y_index = axes.index(selected_x_axis), axes.index(selected_y_axis)
    selected_indices = [x_index, y_index]
    other_indices = [i for i in range(len(axes)) if not i in selected_indices]
    XX = np.array([X.flatten()]).T
    YY = np.array([Y.flatten()]).T
    m=0
    N=len(XX)
    if x_index==0:
        pts= XX 
    elif y_index==0:
        pts=YY
    else:
        pts = np.ones(N)*metamodel_slice_values[0]
        m=1
    for ax_index in range(1,len(axes)):
        if ax_index in other_indices:
            pts = np.c_[pts,np.ones(N)*metamodel_slice_values[m]]
            m+=1
        elif ax_index == x_index:
            pts = np.c_[pts, XX] 
        elif ax_index == y_index:
            pts = np.c_[pts, YY]
    Z = rbf_func(*pts.T).reshape(X.shape)
    p = fig.add_surface(x=x_axis, y=y_axis, z=Z, opacity=0.7, colorscale=st.session_state.colorscale)
    fig.update_coloraxes(showscale=False)
    return fig

@st.cache_data
def fit_a_metamodel(data,train_per,name,meta_params,in_axes,out_axes):
    st.write(f"Fitting {name} metamodel with given params and {train_per} % train data... sampled randomly...")
    st.write(f"input axes = {in_axes}, performance measure (out axes) = {out_axes}")
    num_samples_percent = train_per/100 # num of sample points is num_samples_percent % of whole data we created above
    
    # randomly sample some K training points
    k = int(data.shape[0]*num_samples_percent)
    indices = random.sample(range(0, data.shape[0]), k)
    X_train = data[in_axes].values[indices]
    y_train = data[out_axes].values[indices]
    
    if(name=="GPR"):
        # let us fit a GPR metamodel with RBF kerneli
        kernel = RBF(length_scale=meta_params[0],length_scale_bounds=meta_params[1])
        regr = GaussianProcessRegressor(kernel=kernel,random_state=0).fit(X_train,y_train)
    elif(name=="NN"):
        regr = MLPRegressor(hidden_layer_sizes=np.repeat(meta_params[1],meta_params[0]),
                            activation='relu',
                            solver='lbfgs',
                            random_state=1,
                            max_iter=3000).fit(X_train, y_train)
    st.write("fitted!")
    return regr

def main():
    # Configs and sidebar
    st.set_page_config(
        page_title="DATA vis",
        page_icon="favicon.png",
        layout="wide",
        initial_sidebar_state="expanded")

    st.sidebar.subheader("🚀  [About](#about)")
    st.sidebar.subheader("📃  [Data Setup](#set-up-the-data)")
    st.sidebar.subheader("📊  [Visualize](#visualize)")
    st.sidebar.subheader("📊  [Meta-Models](#build-a-meta-model-from-the-measured-data-points)")
    with st.sidebar:
        c1,c2 = st.columns([10,90])
        with c2:
            marker_size = st.slider("⚙️ Marker size", min_value=1, max_value=10, value=4, step=1,key="marker_size")
            colorscale = st.selectbox(' ⚙️ Color scale',px.colors.named_colorscales(),key="colorscale", index=1) #use 48 for Virdis
    st.sidebar.markdown("---")



    # Main page ====================
    
    st.image("DATA_vis.png",width=400)
    st.subheader("Multi-dimensional Data Visualizer")
    st.caption("A simple tool to visualize samples of vector functions over a multi-dimensional space.")
    st.markdown("""
    DATA vis is particularly useful for visualizing objective function samples in black-box optimization problems. It 
    also creates interpolation Meta-models over the sample values and allows the user to visualize 3D slices 
    of this meta-model using surface plots.
    """
    )

    st.markdown("Made by Neha Karanjkar [(Webpage)](https://nehakaranjkar.github.io/)")
    
    # Data setup ====================
    st.markdown("""---""")
    st.subheader("Set up the data")

    c1,c2=st.columns([40,60])
    with c1:
        data_choice = st.radio("Select a data source:",  ( 'Upload a csv file', 'Generate synthetic data at random points', 'Generate synthetic data along a regular grid'), index=0)

        if data_choice == 'Generate synthetic data at random points':
            num_axes = st.slider("Number of input dimensions (axes)", min_value=2, max_value=10, value=5, step=1)
            num_functions= st.slider("Number of output dimensions (function components)", min_value=2, max_value=10, value=3, step=1)
            num_rows = st.slider("Number of data samples ", min_value=10, max_value=1000, value=100, step=1)
        
        elif data_choice == 'Generate synthetic data along a regular grid':
            num_axes = st.slider("Number of input dimensions (axes)", min_value=2, max_value=10, value=5, step=1)
            num_functions= st.slider("Number of output dimensions (function components)", min_value=2, max_value=10, value=3, step=1)
            num_pts_per_axes = st.slider("Number of points along each axis", min_value=2, max_value=10, value=5, step=1)
            num_rows = num_pts_per_axes**num_axes

        else:
            st.write("The expected format is as shown below. ")
            st.image("data_format.png",width=200)
            st.markdown("""
            The first N columns should contain the N-dimensional coordinate 
            values and the last M columns should contain the values of the M function components at each point.
            The first row should contain the column names.
            """)

    with c2:
        if data_choice == 'Upload a csv file':
            uploaded_file = st.file_uploader("Upload data as a csv file", type="csv")
            if uploaded_file is not None:
                data = load_data(uploaded_file)
                if data.shape[1] < 3:
                    st.error("Error: The uploaded CSV file must have at least 3 columns.")
                    return
                else:
                    st.session_state.data_generated=True
                    st.session_state.data=data
                    with st.expander("View raw data"):
                        st.write(data)

        else:
            if st.button(('Re-Generate!' if 'data_generated' in st.session_state else 'Generate!')):
                if data_choice == 'Generate synthetic data at random points':
                    data,f_names = generate_random_data(num_rows,num_axes,num_functions)
                else:
                    num_rows = (num_pts_per_axes)**num_axes
                    data,f_names = generate_grid_data(num_pts_per_axes,num_axes,num_functions)

                st.write(f"Generating synthetic data with {num_rows} points ...")
                st.session_state.f_names = f_names
                st.session_state.data_generated=True
                st.session_state.data=data
                if 'metamodel_generated' in st.session_state:
                    del st.session_state['metamodel_generated']

            if 'data' in st.session_state:
                data=st.session_state.data
                if 'f_names' in st.session_state:
                    st.markdown(st.session_state.f_names)
                with st.expander("View raw data"):
                    st.write(data)
                st.download_button('Download generated data as a CSV file', to_csv(data), 'sample_data.csv', 'text/csv')

    if 'data' not in st.session_state:
        return
    
    #Visualize =========================
    st.markdown("""---""")
    st.subheader("Visualize")
    
    if st.session_state.data_generated:
        data = st.session_state.data
        column_names=list(data.columns)
        st.write("Select columns corresponding to the point coordinates and function values in your csv file")
        if data_choice != 'Upload a csv file':
            default_axes = column_names[0:num_axes]
        else:
            #default_axes = column_names[5:13]
            default_axes = ['S_R1','s_R1', 'S_R2', 's_R2', 'S_D1', 's_D1', 'S_D2', 's_D2']

        axes = st.multiselect("Columns containing coordinates along each axis:", column_names, default=default_axes)
        default_functions = [f for f in column_names if f not in axes]
        functions = st.multiselect("Columns containing function values:", default_functions, default='avg_net_profit')


        st.write("Select the components to visualize as a 3D slice:")
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_x_axis = st.selectbox("x-axis", axes, index=0)
        with col2:
            selected_y_axis = st.selectbox("y-axis", [a for a in axes if (a!=selected_x_axis)], index=0)
        with col3:
            selected_function = st.selectbox("function component", functions, index=0)
        
        if selected_x_axis == selected_y_axis or selected_y_axis==selected_function or selected_x_axis == selected_function:
            st.error("Please select two distinct axes to visualize the meta-model")
            return 

        st.markdown("""---""")
        col1, col2 = st.columns([20,80])
        with col1:
            # Get the values of the other axes from the user
            other_axes = [i for i in axes if i not in [selected_x_axis, selected_y_axis]]
            values = []
            #center_values = []
            if other_axes:
                st.write("Select the range of values for the other axes")
                for axis in other_axes:
                    min_value = float(data[axis].min())
                    max_value = max(float(data[axis].max()), min_value+1)
                    step_value = (max_value - min_value)/(np.unique(data[axis]).shape[0]-1)
                    #val = st.slider(f"{axis} range", min_value=min_value, max_value=max_value, value=(min_value, max_value))
                    val = st.slider(f"{axis} range", min_value=min_value, max_value=max_value, step=step_value)
                    values.append(val)
                    #center_values.append(float(val[0]+val[1])/2)
           
        with col2:
            data_slice = slice_data(data, other_axes, values)
            if(len(data_slice)==0):
                st.warning(f"The selected slice contains {len(data_slice)} points")
            else:
                st.info(f"The selected slice contains {len(data_slice)} points")
            fig = plot_3d(data_slice, selected_x_axis, selected_y_axis, selected_function)
            st.plotly_chart(fig, use_container_width=True)

    # Build A Meta-model =========================
    st.markdown("""---""")
    st.subheader("Build a Meta-model from the Measured Data Points")
    
    # making two columns of page
    col1, col2 = st.columns([50,50])
    # apply metamodels and optimizers
    with col1:
        # choose an metamodel to fit
        metamodel_name = st.radio(label = "Choose a Metamodel", options = ["GPR","NN"], index=0)
        st.write("How much data should I use to train the model?")
        train_data_per = st.slider(label = "train percent", min_value=25, max_value=100, step=25)
    with col2:
        if(metamodel_name=="GPR"):
            st.write("Select parameter values for kernel (RBF)")
            length = st.number_input(label="length", min_value=0.1, max_value=None)
            length_bounds = st.slider(label="length_bounds", min_value=1.0, max_value=100.0, value=(1.0, 100.0))
            meta_params = [length,length_bounds]
        else:
            st.write("Select parameter values NN Metamodel")
            n_layers = st.number_input(label="Number of hidden layers?", min_value=1, max_value=8)
            n_neurons = st.number_input(label="Number of neurons in a hidden layer?", min_value=8, max_value=32, step=8)
            meta_params = [n_layers,n_neurons]
            
    if st.button('Build a Meta-model'):
        #rbf_functions = interpolate_rbf(data, axes, functions)
        #st.session_state.metamodel_generated = rbf_functions
        regr = fit_a_metamodel(data,train_data_per,metamodel_name,meta_params,axes,functions)
        st.session_state.metamodel_generated = regr
    
    if 'metamodel_generated' in st.session_state:
        col1, col2 = st.columns([20,80])
        with col1:
            # Get the values of the other axes from the user at which the slice of the metamodel is to be plotted
            metamodel_slice_values = []
            values = []
            if other_axes:
                st.write("Select the values for the other axes at which the 3D slice of the meta-model is to be shown")
                for i,axis in enumerate(other_axes):
                    min_value = float(data[axis].min())
                    max_value = max(float(data[axis].max()), min_value+1)
                    step_value = (max_value - min_value)/(np.unique(data[axis]).shape[0]-1)
                    #metamodel_slice_values.append(st.slider(f"{axis} value", min_value=min_value, max_value=max_value, value=center_values[i]))
                    #metamodel_slice_values.append(st.slider(f"{axis} value", min_value=min_value, max_value=max_value, value=values[i]))
                    val = st.slider(f"{axis} value", min_value=min_value, max_value=max_value, step=step_value)
                    values.append(val)

        with col2:
            # first add ascatter plot of the data slice
            #fig = plot_3d(data_slice, selected_x_axis, selected_y_axis, selected_function)
            # select the rbf function corresponding to the selected function component
            #rbf_func = st.session_state.metamodel_generated[functions.index(selected_function)]
            # generate a surface plot of the meta-model (selected component) into fig
            #fig = add_interpolation_surface(fig, data, axes, selected_x_axis, selected_y_axis, rbf_func, metamodel_slice_values)
            #st.plotly_chart(fig, use_container_width=True)
            
            data_slice = slice_data(data, other_axes, values)
            fig = px.scatter_3d(data_slice, x=selected_x_axis, y=selected_y_axis,z=selected_function, color=selected_function, color_continuous_scale=st.session_state.colorscale)
            fig.update_layout(scene = dict(aspectmode='cube'),template='plotly',
                margin={"l":0,"r":0,"t":0,"b":0} 
            )
            fig.update_traces(marker_size=st.session_state.marker_size)  
            
            # make prediction
            predictions = regr.predict(data_slice[axes].values)
            
            unique_vals = len(np.unique(data_slice[selected_x_axis].values))
            z=np.array((predictions))
            z=np.resize(z,(unique_vals,unique_vals))
            x=np.array((data_slice[selected_x_axis].values))
            x=np.resize(x,(unique_vals,unique_vals))
            y=np.array((data_slice[selected_y_axis].values))
            y=np.resize(y,(unique_vals,unique_vals))
            
            p = fig.add_surface(x=x, y=y, z=z, opacity=0.7, colorscale=st.session_state.colorscale)
            fig.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig, use_container_width=True)
if __name__ == "__main__":
    main()