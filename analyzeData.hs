import Data.Function;

-- wI 5; 0.4 0.25 0.125 
weightingInterval :: Int -> Double
weightingInterval n = (fromIntegral 1) / fromIntegral (n + 1)

{-
This function returns an average of a list
such that the values towards the beginning are
given higher weighting than those at the end
-}
weightedAverage :: [Double] -> Double
weightedAverage (x:xs) =
    (sum $ (zipWith(*) (x:xs) [1 - interval, (1 - (2 * interval)) .. 0])) / (fromIntegral(length xs + 1) / 2)
    where interval = (weightingInterval ((length xs) + 1))

percentError :: Double -> Double -> Double
percentError a b = ((a - b) / b) * 100

fluctuation :: [Double] -> Bool
fluctuation (x:xs) = abs (percentError x (weightedAverage xs)) > 15

    


{-

(1 - (1 * 0.2))x +
(1 - (2 * 0.2))x-1 +
(1 - (3 * 0.2))x-2 +
(1 - (4 * 0.2))x-3 

0.8 + 0.6 + 0.4 + 0.2 = 2

1 - 1 * 0.1 +
1 - 2 * 0.1 +
1 - 3 * 0.1 +
1 - 4 * 0.1 +
1 - 5 * 0.1 +
1 - 6 * 0.1 +
1 - 7 * 0.1 +
1 - 8 * 0.1 +
1 - 9 * 0.1

0.9 + 0.8 + 0.7 + 0.6 + 0.5 + 0.4 + 0.3 + 0.2 + 0.1 = 4.5

-}