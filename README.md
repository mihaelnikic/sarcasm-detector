# Seminar-2017

## Introduction

The goal of the seminar is to re-implement the paper : ‘Your Sentiment
Precedes You: Using an author's
historical tweets to predict
sarcasm’. Original paper was written in English, and reimplementation paper in Croatian. Both papers can be found in `docs` folder.

** Abstact: **

Sarcasm understanding may require information beyond the text itself, as in the
case of ‘I absolutely love this restaurant!’
which may be sarcastic, depending on the
contextual situation. We present the first
quantitative evidence to show that historical tweets by an author can provide additional context for sarcasm detection. Our sarcasm detection approach uses two components: a contrast-based predictor (that
identifies if there is a sentiment contrast
within a target tweet), and a historical
tweet-based predictor (that identifies if the
sentiment expressed towards an entity in
the target tweet agrees with sentiment expressed by the author towards that entity in
the past).

## Architecture
The architecture of reimplemented sarcasm detector takes as input the text of a
tweet and the author, and predicts the output as either sarcastic or non-sarcastic.

![](assets/arh_resized)


This is a rule-based
sarcasm detection approach that consists of three
modules:

* Contrast-based Predictor,
* Historical Tweet-based Predictor,
* Integrator.

## Langs & techonlogies

* NLTK
* Python 3.6
* Jupyter Notebook
* Sentiment-Analysis-Vader