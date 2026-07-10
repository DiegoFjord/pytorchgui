# torchui
visualize neural networks

this is is an educational app to help you visualize the components used in a neural network

## whats included
### nn components
- **linearlayer**
- **Dropout**
- **Tril**
- **LayerNorm**
- **ReLU**
- **Mutiplication**
### helper components
- **Batching**
- **Embedding**
- **Split**
- **Scripting**
- **output**
### features
- **dynamic runtime**
- **libraries**

## using torchui
- **Running:** select run to run connected components
- **connecting componets:** click on items to load onto canvas. drag item around using drag and connect using "Line"
- **File** select File to load and save projects, and load libraries. Select File again to close menu
- **Libraries:** 
    - any project can be loaded in as a library as long as it contains a terminate component at the end
    - to load a library select *File > add lib: project name*\
    this will load in the project as a library\
    the library should appear in the second dropdown menu

- **Reset:** clears the active project

## Quick start
To run a basic implementation of a transformer in torchui select *File > load file:"gpt" > Run*\
alternatively run any Library by connecting to Start and Run\
any library can be opened as a regular project to view components

## Component Panel
every component comes with a panel and tunable parameters
- **Start:** 
    - test: forwards an 2x4x16 matrix(change in items.py nnStart)
    - data: the file forwards 1 x n matrix where n is the tokens in the file(tokens made autmatically)
    - entry: used to select file to run
- **Linear:** 
    - scrollbox: set the linear layer width
- **Batch**
    - scrollbox1: set the batch size
    - scrollbox2: set the context size
    - train/validate: N/A
- **Embedding**
    - **NOTE**: use after batch
    - entry: set the embedding size for batch
- **Multiply** 
    - transpose matrices
    - flip order of matrix multiplication
- **Script**
    - entry: operate on input matrix. set x to output
- **Split**
    - scrollbox1: split into n pieces
    - scrollbox2: out put nth piece
- **Tril:** N/A
- **Dropout**
    - set dropout amout from 0-1
- **Terminate**
    - matrix/shape: display matrix or shape of matrix
- **LayerNorm:** N/A
- **ReLU:** N/A
###
\*Batch operates on data from start file\
\*\*Embedding operates on batch output\

