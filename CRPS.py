def CRPS(true_RULs, RUL_distributions, beta = 1.5):
    """
    This function calculates the CRPS and the weighted CRPS.
    Parameters
    ----------
    true_RULs: Dictionary
    A dictionary with for each test instance (key, integer), the true RUL (value).
    RUL_distributions : Dictionary
    A dictionary with for each test instance (key, integer), a list (value) with all RUL predictions
    of this test instance. true_RULs and RUL distributions should have the same set of keys.
    beta : Float between 1 (included) and 2 (included)
    Penalty for overestimating the RUL relative to underestimating the RUL.
    The default is 1.5.
    Returns
    -------
    crps : Float
    The CRPS metric.
    weighted_crps : Float
    The weighted CRPS metric,
    """
    crps_sum = 0 #The value of the sum of the CRPS metric
    weighted_crps_sum = 0 #The value of the sum of the weighted CRPS metric
    #Calculate the CRPS and the weighted CRPS for each individual test instance
    for i in true_RULs.keys():
    #Initiliaze the CRPS and the weighted CRPS for test instance i
        crps_i = 0
        weighted_crps_i = 0
        #Get the probability distribution of the RUL of test instance i, and the true RUL
        distribution = RUL_distributions.get(i)
        true_RUL = true_RULs.get(i)
        distribution.sort()
        number_of_predictions = len(distribution) #The number of RUL predictions in the distribution
        for j in range(0, number_of_predictions -1, 1): #Go over all the predictions
            #Calculate the distance between two RUL predictions
            RUL_prediction = distribution[j]
            next_RUL_prediction = distribution[j+1]
            delta_RUL = next_RUL_prediction - RUL_prediction
            #Each RUL prediction has a probability of 1 over the number of predictions.
            #We use j+1, since j starts at 0, and since we consider the CDF
            probability = (j+1) / number_of_predictions
            #Check if the RUL prediction is larger, or smaller than the true RUL,
            #and update the CRPS and the weighted CRPS accordingly
            # print(RUL_prediction)
            # print(true_RUL)
            if RUL_prediction < true_RUL[j]:
                probability_squared = probability ** 2
                crps_i = crps_i + (probability_squared * delta_RUL)
                weighted_crps_i = weighted_crps_i + (2 - beta) * (probability_squared * delta_RUL)
            else:
                probability_minus_one = probability - 1
                probability_squared = probability_minus_one ** 2
                crps_i = crps_i + (probability_squared * delta_RUL)
                weighted_crps_i = weighted_crps_i + beta * (probability_squared * delta_RUL)
        
        #Also consider the difference between the true RUL and the last prediction
        last_prediction = distribution[-1]
        if last_prediction < true_RUL[-1]:
            crps_i = crps_i + (1 * (true_RUL[-1] - last_prediction))
            weighted_crps_i = weighted_crps_i + (2 -beta) * (1 * (true_RUL[-1] - last_prediction))
            
        #Also consider the difference between the true RUL and the first prediction
        first_prediction = distribution[0]
        if first_prediction > true_RUL[0]:
            crps_i = crps_i + (1 * (first_prediction-true_RUL[0]))
            weighted_crps_i = weighted_crps_i + beta * (1 * (first_prediction-true_RUL[0]))
        #Update the sum of the CRPS and the sum of the weighted CRPS
        crps_sum = crps_sum + crps_i
        weighted_crps_sum = weighted_crps_sum + weighted_crps_i
    #Take the average value of the CRPS and the weighted CRPS
    crps = crps_sum / len(RUL_distributions.keys())
    weighted_crps = weighted_crps_sum / len(RUL_distributions.keys())
    return crps, weighted_crps
