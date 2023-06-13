import argparse
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

N = 10000

LABEL_NORMAL = 1
LABEL_ATTACK = -1

FEATURES = [
    'Duration',
    'Source bytes',
    'Destination bytes',
    'Count',
    'Same_srv_rate',
    'Serror_rate',
    'Srv_serror_rate',
    'Dst_host_count',
    'Dst_host_srv_count',
    'Dst_host_same_src_port_rate',
    'Dst_host_serror_rate',
    'Dst_host_srv_serror_rate',
]

def fix_dataset(file_path):
    df = pd.read_csv(file_path)
    # データフレームのうちラベルが正常のもの
    normal = df[df.Label == LABEL_NORMAL]
    # 正常なものについて使用する特徴量のみを切り出してサンプリング
    normal = normal.loc[:, FEATURES].sample(N)

    # データフレームのうちラベルが攻撃のもの
    attack = df[df.Label == LABEL_ATTACK]
    # 攻撃について使用する特徴量のみを切り出してサンプリング
    # クラスごとのサンプル数が不均衡なのは望ましくないので同数にします
    attack = attack.loc[:, FEATURES].sample(N)

    label = [LABEL_NORMAL] * len(normal) + [LABEL_ATTACK] * len(attack)
    print('正常 : {}, 攻撃 : {}'.format(normal.shape, attack.shape))

    return pd.concat((normal, attack)), label

# ディレクトリとファイルのパスを指定
csv_directory = "./seminar/data/buf"

parser = argparse.ArgumentParser()
parser.add_argument("train_date", help="Training date in the format YYYYMMDD")
parser.add_argument("test_date", help="Testing date in the format YYYYMMDD")
args = parser.parse_args()

# 学習用データのCSVファイルパスを作成
train_csv_file = f"{csv_directory}/{args.train_date}.csv"

# テスト用データのCSVファイルパスを作成
test_csv_file = f"{csv_directory}/{args.test_date}.csv"

# 学習用データを読み込む
train_data, train_data_label = fix_dataset(train_csv_file)

# テスト用データを読み込む
test_data, test_data_label = fix_dataset(test_csv_file)

# ランダムフォレストモデルを作成してトレーニングする
model = RandomForestClassifier()
model.fit(train_data, train_data_label)

# テストデータを使って予測を行う
y_pred = model.predict(test_data)

# 予測の精度を評価する
accuracy = accuracy_score(test_data_label, y_pred)
print("Accuracy:", accuracy)




