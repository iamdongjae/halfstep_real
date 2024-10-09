import os
import torch
import numpy as np
import gluonnlp as nlp
from transformers import AdamW

from kobert.bert_classifier import BERTClassifier
from kobert.bert_dataset import BERTDataset
from kobert_tokenizer import KoBERTTokenizer
from transformers import BertModel

# KOBERT 모델 클래스 
class kobert_model:
    # 생성자 (매개변수는 모델 파일들의 경로, 없을 경우 현재 디렉토리로 설정함.)
    def __init__(self, base_dir:str=None):
        if base_dir == None:
            base_dir = "./"
        model_dir = os.path.join(base_dir, 'models')

        # 사전 훈련된 BERTMODEL은 SKT Brain팀의 한국어 자연어 처리 모델로 지정하여 다운로드
        bertmodel = BertModel.from_pretrained('skt/kobert-base-v1', return_dict=False)

        # GPU가 있으면 cuda, 없으면 cpu
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

        # BERT 모델 불러오기.
        self.model = BERTClassifier(bertmodel, dr_rate=0.5).to(self.device)

        # 데이터는 사전 훈련된 모델 파일들을 로딩한다.
        # 사전 훈련된 모델 데이터는 7가지 감성으로 훈련됨 - 공포, 놀람, 분노, 슬픔, 중립, 행복, 혐오.
        self.model.load_state_dict(torch.load(os.path.join(model_dir,'7emotions_model_state_dict.pt'), map_location=self.device))
        checkpoint = torch.load(os.path.join(model_dir,'7emotions_all.tar'), map_location=self.device)
        self.model.load_state_dict(checkpoint['model'])

        learning_rate =  5e-5
        tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')
        self.tok = tokenizer.tokenize
        self.vocab = nlp.vocab.BERTVocab.from_sentencepiece(tokenizer.vocab_file, padding_token='[PAD]')

        # optimizer와 schedule 설정.
        no_decay = ['bias', 'LayerNorm.weight']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in self.model.named_parameters() if not any(nd in n for nd in no_decay)], 'weight_decay': 0.01},
            {'params': [p for n, p in self.model.named_parameters() if any(nd in n for nd in no_decay)], 'weight_decay': 0.0}
        ]
        optimizer = AdamW(optimizer_grouped_parameters, lr = learning_rate)
        optimizer.load_state_dict(checkpoint['optimizer'])

    # 입력된 문장의 감성을 분석하는 멤버 함수.
    def predict(self, predict_sentence): # input = 감정분류하고자 하는 sentence
        max_len = 64
        batch_size = 64
        data = [predict_sentence, '0']
        dataset_another = [data]

        another_test = BERTDataset(dataset_another, 0, 1, self.tok, self.vocab, max_len, True, False) # 토큰화한 문장
        test_dataloader = torch.utils.data.DataLoader(another_test, batch_size = batch_size, num_workers = 5) # torch 형식 변환

        self.model.eval()

        for batch_id, (token_ids, valid_length, segment_ids, label) in enumerate(test_dataloader):
            token_ids = token_ids.long().to(self.device)
            segment_ids = segment_ids.long().to(self.device)

            valid_length = valid_length
            label = label.long().to(self.device)

            out = self.model(token_ids, valid_length, segment_ids)

            test_eval = []
            for i in out: # out = model(token_ids, valid_length, segment_ids)
                logits = i
                logits = logits.detach().cpu().numpy()

                if np.argmax(logits) == 0:
                    test_eval.append("공포")
                elif np.argmax(logits) == 1:
                    test_eval.append("놀람")
                elif np.argmax(logits) == 2:
                    test_eval.append("분노")
                elif np.argmax(logits) == 3:
                    test_eval.append("슬픔")
                elif np.argmax(logits) == 4:
                    test_eval.append("중립")
                elif np.argmax(logits) == 5:
                    test_eval.append("행복")
                elif np.argmax(logits) == 6:
                    test_eval.append("혐오")
            return test_eval[0]

