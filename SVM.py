from svmutil import *

def trainSVMModel(vectorPath = './vector.txt',modelPath = './model.txt'):
    y,x = svm_read_problem(vectorPath)
    model = svm_train(y,x,'-c 4')
    svm_save_model(modelPath,model)

def testSVMModel(testPath = './vector.txt', modelPath = './model.txt'):
    y,x = svm_read_problem(testPath)
    model = svm_load_model(modelPath)
    p_label, p_acc, p_val = svm_predict(y,x,model)
    return p_label
