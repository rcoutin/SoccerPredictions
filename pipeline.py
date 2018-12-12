from models import keras_1, keras_2
from sklearn.model_selection import train_test_split

# train a feats model
from gen_feats_data import get_feats_tr_data, tr_cols

feats_tr_data = get_feats_tr_data()
x_train,x_test,y_train,y_test = train_test_split(feats_tr_data[tr_cols()],feats_tr_data['Result'],test_size = 25,statify = feats_tr_data['Result'] )

print(x_train)








# # train field pos model
# from gen_fieldpos_data import get_fieldpos_tr_data, tr_cols


