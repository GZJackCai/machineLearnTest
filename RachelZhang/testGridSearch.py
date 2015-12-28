# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
#first extract the 20 news_group dataset to /scikit_learn_data
from sklearn.datasets import fetch_20newsgroups
#all categories
#newsgroup_train = fetch_20newsgroups(subset='train')
#part categories
categories = ['comp.graphics',
 'comp.os.ms-windows.misc',
 'comp.sys.ibm.pc.hardware',
 'comp.sys.mac.hardware',
 'comp.windows.x'];
newsgroup_train = fetch_20newsgroups(subset = 'train',categories = categories);
newsgroups_test = fetch_20newsgroups(subset = 'test',categories = categories);

#（准确率*召回率）/（准确率+召回率）
def calculate_result(actual,pred):
    m_precision = metrics.precision_score(actual,pred);
    m_recall = metrics.recall_score(actual,pred);
    print 'predict info:'
    print 'precision:{0:.3f}'.format(m_precision)
    print 'recall:{0:0.3f}'.format(m_recall);
    print 'f1-score:{0:.3f}'.format(metrics.f1_score(actual,pred));


print '*************************\nFeature Extraction\n*************************'
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.grid_search import GridSearchCV
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer

pipeline = Pipeline([
('vect',CountVectorizer()),
('tfidf',TfidfTransformer()),
('clf',SGDClassifier()),
]);

parameters = {
    'vect__max_df': (0.5, 0.75),
    'vect__max_features': (None, 5000, 10000),
    'tfidf__use_idf': (True, False),
#    'tfidf__norm': ('l1', 'l2'),
    'clf__alpha': (0.00001, 0.000001),
#    'clf__penalty': ('l2', 'elasticnet'),
    'clf__n_iter': (10, 50),
}


#gridsearch寻找vectorizer词频统计, tfidftransformer特征变换和SGD classifier的最优参数
grid_search = GridSearchCV(pipeline,parameters,n_jobs = 1,verbose=1);
print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline.steps])
print("parameters:")
print(parameters)
from time import time
t0 = time()
grid_search.fit(newsgroup_train.data, newsgroup_train.target)
print("done in %0.3fs" % (time() - t0))
print()
print("Best score: %0.3f" % grid_search.best_score_)

#3. 输出最佳参数，在此基础上求最佳结果
from sklearn import metrics
best_parameters = dict();
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]));
pipeline.set_params(clf__alpha = 1e-05,
                    clf__n_iter = 50,
                    tfidf__use_idf = True,
                    vect__max_df = 0.5,
                    vect__max_features = None);
pipeline.fit(newsgroup_train.data, newsgroup_train.target);
pred = pipeline.predict(newsgroups_test.data)
calculate_result(newsgroups_test.target,pred);