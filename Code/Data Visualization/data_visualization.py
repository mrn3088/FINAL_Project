# -*- coding: utf-8 -*-
"""data_visualization.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15sdPa4M3YdBDFI9E7aEUJHVRjvKCWyx3
"""

import pandas as pd
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
import librosa
import librosa.display

df = pd.read_csv('drive/MyDrive/data/features_3_sec.csv')
df.head(5)

import seaborn as sns
from sklearn.model_selection import train_test_split
df_train, df_test = train_test_split(df, test_size=0.2)

sns.set(rc={'figure.figsize':(11.7,8.27)})
sns.histplot(data = df, x = 'label');
plt.title('Distribution of Each Genre in Dataset', fontsize = 15);

# pretent we do train/test split with 800 train and 200 test
sns.histplot(data = df_train, x = 'label');
plt.title('Distribution of Each Genre in Training Data', fontsize = 15);

sns.histplot(data = df_test, x = 'label');
plt.title('Distribution of Each Genre in Testing Data', fontsize = 15);

sns.scatterplot(data = df, x = "chroma_stft_mean", y = "chroma_stft_var", hue = "label", alpha = 0.5, palette = "Paired", s = 20);
plt.title('Relation Between mean of chroma_stft and variance of chroma_stft ', fontsize = 15);

sns.scatterplot(data = df, x="rms_mean", y="rms_var", hue="label", alpha = 0.9, palette = "mako", s = 10);

sns.boxplot(y = "label", x = "tempo", data = df, orient = "h", palette = "pastel");
plt.title('Range of How Fast Different Genres of Music is Played', fontsize = 15);

#getting all mean columns
cols = []
for col in df.columns:
  if 'mean' in col:
    cols.append(col)

# Calculating their correlation between one another, including with themselves
correlation = df[cols].corr()

# Generate a numpy array with 1s with the same shape as the correlation matrix 
# Make the upper half above the diagonal line 0s
# Generate a mask for the upper triangle, making all correlation matrix upper half 0s
upper_mask = np.triu(np.ones_like(correlation))

# Define the colors will be used
cmap = sns.diverging_palette(220, 300, as_cmap=True)

# Generate the heatmap
sns.heatmap(correlation, mask = upper_mask, cmap = cmap, square = True);

plt.title('Correlation Heatmap for the mean variables', fontsize = 15);

# Doing the same things for variance variables

cols_var = []
for col_var in df.columns:
  if 'var' in col_var:
    cols_var.append(col_var)

correlation_var = df[cols_var].corr()

upper_mask = np.triu(np.ones_like(correlation_var))

cmap = sns.diverging_palette(0, 220, as_cmap=True)

sns.heatmap(correlation_var, mask = upper_mask, cmap = cmap, square = True);

plt.title('Correlation Heatmap for Varaince variables', fontsize = 15);

select_col = df.columns[19:59]
df_mfcc = df[select_col]
df_mfcc['filename'] = df['filename']
df_mfcc['label'] = df['label']
df_mfcc

mfcc_mean = []
for col in df_mfcc.columns:
  if 'mean' in col:
    mfcc_mean.append(col)

df_mfcc_mean = df_mfcc[mfcc_mean]
df_mfcc_mean['filename'] = df_mfcc['filename']
df_mfcc_mean['label'] = df_mfcc['label']

df_mfcc_mean = df_mfcc_mean.groupby(['label']).mean()
df_mfcc_mean.reset_index(inplace = True)
df_mfcc_mean

mfcc_var = []
for col in df_mfcc.columns:
  if 'var' in col:
    mfcc_var.append(col)

df_mfcc_var = df_mfcc[mfcc_var]
df_mfcc_var['filename'] = df_mfcc['filename']
df_mfcc_var['label'] = df_mfcc['label']

df_mfcc_var = df_mfcc_var.groupby(['label']).mean()
df_mfcc_var.reset_index(inplace = True)
df_mfcc_var

df_mfcc_mean_long = pd.melt(df_mfcc_mean, id_vars=['label'],
                            value_vars=None, var_name='mfcc',
                            value_name='mean',
                            col_level=None, 
                            ignore_index=True)

df_mfcc_var_long = pd.melt(df_mfcc_var,
                           id_vars=['label'],
                           value_vars=None,
                           var_name='mfcc',
                           value_name='var',
                           col_level=None,
                           ignore_index=True)

sns.lineplot(data = df_mfcc_mean_long, x = 'mfcc', y = 'mean', hue = 'label', palette = "Paired");
plt.xticks(rotation = 45);
plt.title('Mean Calculated for Each Genre\'s of MFCC means Plotted in Time Order', fontsize = 15);

sns.lineplot(data = df_mfcc_var_long, x = 'mfcc', y = 'var', hue = 'label', palette = "Paired");
plt.xticks(rotation = 45);
plt.title('Mean Calculated for Each Genre\'s of MFCC variance Plotted in Time Order', fontsize = 15);

from sklearn import preprocessing

data = df.iloc[0:, 1:]
y = data['label']
X = data.loc[:, data.columns != 'label']

#### NORMALIZE X ####
cols = X.columns
min_max_scaler = preprocessing.MinMaxScaler()
np_scaled = min_max_scaler.fit_transform(X)
X = pd.DataFrame(np_scaled, columns = cols)


#### PCA 2 COMPONENTS ####
from sklearn.decomposition import PCA

pca = PCA(n_components = 2)
principalComponents = pca.fit_transform(X)
principalDf = pd.DataFrame(data = principalComponents, columns = ['principal component 1', 'principal component 2'])

# concatenate with target label
finalDf = pd.concat([principalDf, y], axis = 1)

pca.explained_variance_ratio_

plt.figure(figsize = (16, 9))
sns.scatterplot(x = "principal component 1", y = "principal component 2", data = finalDf, hue = "label", alpha = 0.7, s = 20, palette = "Paired");

plt.title('PCA on Genres', fontsize = 15)
plt.xticks(fontsize = 14)
plt.yticks(fontsize = 10);
plt.xlabel("Principal Component 1", fontsize = 15)
plt.ylabel("Principal Component 2", fontsize = 15)
plt.savefig("PCA Scattert.jpg")

signal, sr = librosa.load('drive/MyDrive/data/genres_original/blues/blues.00005.wav')

plt.figure(figsize = (16, 4))
librosa.display.waveplot(signal, sr);
plt.title('Blues.00005 Waveplot', fontdict = dict(size = 15));
plt.xlabel('Time');
plt.ylabel('Amplitude');

plt.figure(figsize = (16, 4))
librosa.display.waveshow(signal, sr = sr, alpha = 0.4);

stft_abs = np.abs(librosa.stft(signal))
plt.figure(figsize = (16, 4))
librosa.display.specshow(stft_abs, sr = sr, x_axis = 'time', y_axis = 'hz');
plt.ylabel('Frequency')
plt.colorbar();

stft_db = librosa.amplitude_to_db(stft_abs)
plt.figure(figsize = (16, 4))
librosa.display.specshow(stft_db, sr = sr, x_axis = 'time', y_axis = 'hz')
plt.ylabel('Frequency')
plt.colorbar();

chroma = librosa.feature.chroma_stft(signal, sr = sr)
plt.figure(figsize=(16, 4))
librosa.display.specshow(chroma, sr = sr, x_axis = 'time', y_axis = 'chroma', cmap = 'coolwarm')
plt.colorbar()
plt.title('Chroma Features');

mfccs = librosa.feature.mfcc(y = signal, sr = sr, n_mfcc = 20)
plt.figure(figsize=(16, 4))
librosa.display.specshow(mfccs);
plt.colorbar()
plt.title('Mel-frequency Cepstral Coefficients');

plt.figure(figsize=(16, 4))
plt.plot(signal[512:1024]);
plt.grid()

# Load the audio data
y, sr = librosa.load('drive/MyDrive/data/genres_original/blues/blues.00005.wav')


length = librosa.get_duration(y=y, sr=sr)
chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)

rms = librosa.feature.rms(y=y) 
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr) 
spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr) 

rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
harmony = librosa.effects.harmonic(y=y)
tempo = librosa.beat.tempo(y=y,sr=sr)
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
plp = librosa.beat.plp(y=y,sr=sr)

# Create a dataframe with the features
data = {"filename": ['drive/MyDrive/data/genres_original/blues/blues.00005.wav'],
        "length": [length],
        "chroma_stft_mean": [np.mean(chroma_stft)],
        "chroma_stft_var": [np.var(chroma_stft.var())],
        "rms_mean": [rms.mean()],
        "rms_var": [rms.var()],
        "spectral_centroid_mean": [spectral_centroid.mean()],
        "spectral_centroid_var": [spectral_centroid.var()],
        "spectral_bandwidth_mean": [spectral_bandwidth.mean()],
        "spectral_bandwidth_var": [spectral_bandwidth.var()],
        "rolloff_mean": [rolloff.mean()],
        "rolloff_var": [rolloff.var()],
        "zero_crossing_rate_mean": [zero_crossing_rate.mean()],
        "zero_crossing_rate_var": [zero_crossing_rate.var()],
        "harmony_mean": [harmony.mean()],
        "harmony_var": [harmony.var()],
        "tempo_mean": [tempo.mean()],
        "tempo_var": [tempo.var()],
        "plp_mean": [plp.mean()],
        "plp_var": [plp.var()],
        "mfcc1_mean": [mfccs[0].mean()],
        "mfcc1_var": [mfccs[0].var()],
        "mfcc2_mean": [mfccs[1].mean()],
        "mfcc2_var": [mfccs[1].var()],
        "mfcc3_mean": [mfccs[2].mean()],
        "mfcc3_var": [mfccs[2].var()],
        "mfcc4_mean": [mfccs[3].mean()],
        "mfcc4_var": [mfccs[3].var()],
        "mfcc5_mean": [mfccs[4].mean()],
        "mfcc5_var": [mfccs[4].var()],
        "mfcc6_mean": [mfccs[5].mean()],
        "mfcc6_var": [mfccs[5].var()],
        "mfcc7_mean": [mfccs[6].mean()],
        "mfcc7_var": [mfccs[6].var()],
        "mfcc8_mean": [mfccs[7].mean()],
        "mfcc8_var": [mfccs[7].var()],
        "mfcc9_mean": [mfccs[8].mean()],
        "mfcc9_var": [mfccs[8].var()],
        "mfcc10_mean": [mfccs[9].mean()],
        "mfcc10_var": [mfccs[9].var()],
        "mfcc11_mean": [mfccs[10].mean()],
        "mfcc11_var": [mfccs[10].var()],
        "mfcc12_mean": [mfccs[11].mean()],
        "mfcc12_var": [mfccs[11].var()],
        "mfcc13_mean": [mfccs[12].mean()],
        "mfcc13_var": [mfccs[12].var()],
        "mfcc14_mean": [mfccs[13].mean()],
        "mfcc14_var": [mfccs[13].var()],
        "mfcc15_mean": [mfccs[14].mean()],
        "mfcc15_var": [mfccs[14].var()],
        "mfcc16_mean": [mfccs[15].mean()],
        "mfcc16_var": [mfccs[15].var()],
        "mfcc17_mean": [mfccs[16].mean()],
        "mfcc17_var": [mfccs[16].var()],
        "mfcc18_mean": [mfccs[17].mean()],
        "mfcc18_var": [mfccs[17].var()],
        "mfcc19_mean": [mfccs[18].mean()],
        "mfcc19_var": [mfccs[18].var()],
        "mfcc20_mean": [mfccs[19].mean()],
        "mfcc20_var": [mfccs[19].var()]
        }

df_single = pd.DataFrame(data)

# Save the dataframe to a .csv file
#df.to_csv("feature_data/features_3_sec.csv", index=False)

df_single

