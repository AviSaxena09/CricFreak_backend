"""This File Contain class to containing functions to call predict function of all the models"""
import pandas as pd


class Prediction:
    """This class conatins all the methods for predictions"""
    @staticmethod
    def predict_course(mod, val):
        """
        :param mod:
        :param val:
        :return:
        """
        return int(mod.predict(val)[0])

    @staticmethod
    def predict_wicket(mod_knn, mod_svm, val, curr_over):
        """
        :param mod_knn:
        :param mod_svm:
        :param val:
        :param curr_over:
        :return:
        """
        if val[0][12] != float(curr_over):
            return '{"Error" : "Unexpected Error"}'
        curr_over = int(float(curr_over) + 1)
        pred1 = list()
        pred2 = list()
        for wic in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]:
            val[0][12] = curr_over + wic
            pred1.append(mod_knn.predict(val)[0])
            pred2.append(mod_svm.predict(val)[0])

        return Prediction.get_wicket_json(pred1, pred2, curr_over)

    @staticmethod
    def get_wicket_json(pred1, pred2, over_no):
        """
        :param pred1:
        :param pred2:
        :param over_no:
        :return:
        """
        predic = pd.DataFrame([[1, 2, 3, 4, 5, 6], pred1, pred2, ]).T
        predic.columns = ['bno', 'knn', 'svm']
        predic['or_pred'] = predic['knn'] | predic['svm']
        predic['and_pred'] = predic['knn'] & predic['svm']
        predic["sum_pred"] = predic[['knn', 'svm', 'or_pred', 'and_pred']].sum(axis=1)
        if predic['sum_pred'].sum():
            predic["percen_pd"] = (predic['sum_pred'] / (predic['sum_pred'].sum())) * 100
        else:
            predic["percen_pd"] = round(100 / 6, 2)
        b_data = predic[['bno', 'percen_pd']].to_json(orient='records')
        if (list(predic['or_pred']).count(1) == 0) & (list(predic['and_pred']).count(1) == 0):
            expected_wix = "low"
        elif (list(predic['or_pred']).count(1) > 0) & (list(predic['and_pred']).count(1) > 0):
            expected_wix = "high"
        elif (list(predic['or_pred']).count(1) > 0) | (list(predic['and_pred']).count(1) > 0):
            expected_wix = "medium"
        b_data = '[' + '{ "over_number" : ' + str(
            over_no) + '},' + '{ "risk" : "' + expected_wix +\
                 '" },' + '{ "ball_data" : ' + b_data + '}' + ']'
        return b_data
