import json

def create_json():
    data={}
    data['cachedir'] = './kogpt2/'

    data['save_model_path'] = './checkpoint/'

    data['kogpt2_config'] = {
        "initializer_range": 0.02,
        "layer_norm_epsilon": 1e-05,
        "n_ctx": 1024,
        "n_embd": 768,
        "n_head": 12,
        "n_layer": 12,
        "n_positions": 1024,
        "vocab_size": 51200
    }

    data['train_flg'] = True

    data['data_file_path'] = '/content/drive/MyDrive/Colab Notebooks/create_data/use_data/dataset_2.txt'

    data['batch_size'] = 2

    data['epochs'] = 200

    data['learning_rates'] = [1e-4, 5e-5, 2.5e-5, 2e-5]

    data['pretrained_model'] = ''
    print(data)

    with open('config_json.json', 'w') as outfile:
        json.dump(data, outfile)


# with open('Korean-Story-Generator\config_json.json') as f:
#     data = json.load(f)
#     print(data['kogpt2_config'])

create_json()