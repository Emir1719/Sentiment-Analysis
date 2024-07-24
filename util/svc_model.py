import logging
import joblib
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from util.stopwords import StopWords
from util.data_processing import DataProcessing
import seaborn as sns

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SvcModel:
    def __init__(self):
        self.file_path = None
        self.max_features = 18000
        self.data = None
        self.stopwords = StopWords().turkishWords
        self.pipeline = self.create_pipeline()
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.best_model = None

    # Fonksiyonlar
    def load_data(self, file_path):
        """Belirtilen yoldaki veri setini yükler"""
        
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        return self.data

    def train_test_data_split(self, test_size=0.3, random_state=42):
        if self.data is not None:
            process = DataProcessing()
            self.data['comment'] = self.data['comment'].apply(process.clean_text)

            x = self.data['comment']
            y = self.data['type']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(x, y, test_size=test_size, random_state=random_state)
            return self.X_train, self.X_test, self.y_train, self.y_test
        else:
            return None, None, None, None

    # Pipeline oluşturma
    def create_pipeline(self):
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=self.max_features, stop_words=self.stopwords)),
            ('svm', SVC(random_state=42, class_weight='balanced'))
        ])
        return pipeline

    # GridSearchCV ile model optimizasyonu
    def optimize_model(self):
        param_grid = {
            'svm__C': [1, 10],
            'svm__gamma': [0.01, 0.1, 1],
            'svm__kernel': ['linear', 'rbf']
        }
        grid_search = GridSearchCV(self.pipeline, param_grid, cv=5, n_jobs=-1, verbose=3)
        logger.info("Model eğitimi başlatılıyor...")
        grid_search.fit(self.X_train, self.y_train)
        self.best_model = grid_search.best_estimator_

        logger.info(f"En iyi parametreler: {grid_search.best_params_}")

        # GridSearchCV sonuçlarının detaylarını yazdırma
        results = grid_search.cv_results_
        for mean, std, params in zip(results['mean_test_score'], results['std_test_score'], results['params']):
            logger.info(f"Mean: {mean:.3f}, Std: {std:.3f}, Params: {params}")

        return grid_search

    # Performans değerlendirme
    def evaluate_model(self):
        y_pred = self.best_model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        print(f"Accuracy: {accuracy:.3f}")
        return accuracy
    
    # Classification report oluşturma
    def classification_report(self):
        y_pred = self.best_model.predict(self.X_test)
        report = classification_report(self.y_test, y_pred)
        return report

    # Bir cümlenin duygu değerini döndürme
    def predict(self, sentence):
        if self.best_model is None:
            raise ValueError("Model henüz optimize edilmedi ve eğitilmedi.")
        
        sentence_transformed = self.best_model.named_steps['tfidf'].transform([sentence])
        prediction = self.best_model.named_steps['svm'].predict(sentence_transformed)
        return prediction[0]
    
    # Modeli kaydetme
    def save_model(self, file_name):
        if self.best_model is None:
            raise ValueError("Model henüz optimize edilmedi ve eğitilmedi.")
        
        joblib.dump(self.best_model, file_name)
        print(f"Model saved to {file_name}")

    # Modeli yükleme
    def load_model(self, file_name):
        self.best_model = joblib.load(file_name)
        self.pipeline = self.best_model  # pipeline'ı ayarla
        print(f"Model loaded from {file_name}")

    # Karışıklık matrisi çizimi
    def plot_confusion_matrix(self):
        y_pred = self.best_model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)
        cm_df = pd.DataFrame(cm, index=self.best_model.classes_, columns=self.best_model.classes_)
        
        plt.figure(figsize=(10, 7))
        sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
        plt.ylabel('Gerçek Etiketler')
        plt.xlabel('Tahmin Edilen Etiketler')
        plt.title('Karışıklık Matrisi')
        plt.show()
    
    # En sık yapılan yanlış sınıflandırmaların grafiği
    def plot_common_misclassifications(self):
        y_pred = self.best_model.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)
        cm_df = pd.DataFrame(cm, index=self.best_model.classes_, columns=self.best_model.classes_)
        
        misclassifications = pd.DataFrame(columns=['Gerçek', 'Tahmin', 'Sayı'])
        for actual in cm_df.index:
            for predicted in cm_df.columns:
                if actual != predicted:
                    misclassifications = pd.concat([misclassifications, pd.DataFrame({'Gerçek': [actual], 'Tahmin': [predicted], 'Sayı': [cm_df.loc[actual, predicted]]})], ignore_index=True)
        
        misclassifications['Sayı'] = misclassifications['Sayı'].astype(int)
        most_common_misclassifications = misclassifications.loc[misclassifications.groupby('Gerçek')['Sayı'].idxmax()].reset_index(drop=True)
        
        plt.figure(figsize=(10, 7))
        sns.barplot(x='Gerçek', y='Sayı', hue='Tahmin', data=most_common_misclassifications, dodge=False)
        plt.ylabel('Sayı')
        plt.xlabel('Gerçek Kategori')
        plt.title('En Sık Yapılan Yanlış Sınıflandırmalar')
        plt.legend(title='Tahmin Edilen Kategori')
        plt.show()