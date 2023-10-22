from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os, sys, Levenshtein, time,random
import streamlit as st
from urllib.error import URLError
from scipy.spatial import distance
