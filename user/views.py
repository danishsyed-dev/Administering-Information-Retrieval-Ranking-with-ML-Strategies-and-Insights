from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from user.forms import registrationform
from user.models import registrationmodel, WeightModel
import re
from collections import Counter
from django.conf import settings
import pandas as pd
import numpy as np
import inflect
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# We make sure nltk downloads are run at startup or when views are imported
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    print("NLTK download failed:", str(e))

def user(request):
    return render(request, 'user/userlogin.html')

def userregistration(request):
    if request.method == 'POST':
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'you are successfully registred')
            return HttpResponseRedirect('/user/')
        else:
            print('Invalid')
    else:
        form = registrationform()
    return render(request, "user/userregistration.html", {'form': form})

def userloginaction(request):
    if request.method == 'POST':
        usid = request.POST.get('mail')
        print(usid)
        pswd = request.POST.get('password')
        print(pswd)
        try:
            check = registrationmodel.objects.get(email=usid, password=pswd)
            request.session['userid'] = check.loginid
            status = check.status
            print(status)
            if status == "activated":
                print("hello")
                request.session['email'] = check.email
                print("hai-hello")
                return render(request, 'user/userpage.html')
            else:
                messages.success(request, 'user is not activated')
                return render(request, 'user/userlogin.html')
        except Exception as e:
            print('Exception is ', str(e))
            messages.success(request, 'Invalid user id and password')
        return render(request, 'user/userlogin.html')

def home(request):
    return render(request, 'user/userpage.html')

def weight(request):
    if request.method == "GET":
        file = request.GET.get('filename')
        print("file", file)
        head, fileName = os.path.split(file)
        print(type(fileName))

        # Use os.path.join for clean, cross-platform paths
        fPath = os.path.join(settings.MEDIA_ROOT, 'files', 'pdfs', fileName)
        print("hello:", fPath)
        
        try:
            with open(fPath, 'r', encoding='utf-8') as f:
                texts = f.read()
        except UnicodeDecodeError:
            with open(fPath, 'r', encoding='latin-1') as f:
                texts = f.read()
        except Exception as e:
            print("File read error:", str(e))
            return render(request, "user/weight.html", {"dict": 0.0, "error": "Unable to read file."})

        print("reading started")
        lower_text = texts.lower()
        rem_spe = re.sub(r'[^\w\s]', '', lower_text)

        p = inflect.engine()
        num_text = re.sub(r'\d+', lambda m: p.number_to_words(m.group()), rem_spe)
        num_text_processed = re.sub(r'[_,\-]', '', num_text)

        processed = re.sub(r'[ ]+', ' ', num_text_processed)
        processed = re.sub(r'\n[\n]+', '\n', processed)

        stripped = processed.strip()
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()

        articles = [
            " ".join([
                lemmatizer.lemmatize(word)
                for word in word_tokenize(s)
                if word not in stop_words
            ]) for s in stripped.split('\n') if s.strip()
        ]
        
        if not articles or all(not art.strip() for art in articles):
            # Fallback for empty files
            articles = ["empty document"]

        print(articles[:9])
        
        # Generate bag of words object with maximum vocab size of 1000
        counter = CountVectorizer(max_features=1000)
        bag_of_words = counter.fit_transform(articles)
        count_matrix = pd.DataFrame(bag_of_words.todense(), columns=counter.get_feature_names_out())

        # Generate tf-idf object with maximum vocab size of 1000
        # Set min_df to 1 in case the uploaded document is small/single-sentence
        tf_counter = TfidfVectorizer(max_features=1000, min_df=1, max_df=1.0)
        tfidf = tf_counter.fit_transform(articles)
        dataset = pd.DataFrame(tfidf.toarray(), columns=tf_counter.get_feature_names_out())

        print(dataset.astype(bool).sum(axis=0).sort_values(ascending=False))

        processed_articles = [
            [
                x
                for x in a.split()
                if x in tf_counter.get_feature_names_out()
            ] for a in articles
        ]
        print("final data:", processed_articles)
        
        from gensim import corpora, models
        dictionary = corpora.Dictionary(processed_articles)
        corpus = [dictionary.doc2bow(text) for text in processed_articles]

        ldamodel = models.ldamodel.LdaModel(corpus, num_topics=4, id2word=dictionary, passes=20)
        ldamodel.get_topics()
        ldamodel.print_topics()

        print("hello im final data")
        doc_topics = list(ldamodel.get_document_topics(corpus))
        a1 = []
        a2 = []
        for x in doc_topics:
            for y in x:
                a1.append(y)
        for i in a1:
            a2.append(i[1])

        s = sum(a2)
        print("Sum of topic distributions:", s)
        
        # Save calculated weight to wgt database table so that admin can train SVM on it
        WeightModel.objects.create(weight=s)
        
        return render(request, "user/weight.html", {"dict": s})

def frgt(request):
    if request.method == 'POST':
        mail = request.POST.get('e1')
        print(mail)
        mbl = request.POST.get('m1')
        print(mbl)
        print("hello")
        qs = registrationmodel.objects.filter(email=mail, mobile=mbl)
        if qs.exists():
            return render(request, 'user/user1.html', {"msg": mail})
        else:
            return render(request, 'frgt.html', {"hello": "mail doesn't exist or number invalied"})
    else:
        return render(request, 'frgt.html')

def nwpwd(request):
    if request.method == 'POST':
        pwd1 = request.POST.get('p1')
        mail = request.POST.get('name1')
        print("passwd:", pwd1)
        print("mail:", mail)
        qs = registrationmodel.objects.filter(email=mail).update(password=pwd1)
        print(qs)
        return render(request, 'user/user2.html', {"msg": "successfully updated password"})
    else:
        return render(request, 'user/user1.html')
