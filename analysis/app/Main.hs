module Main where

import Analysis

main :: IO ()
main = print $ suggestedAction 7 [4, 3, 5, 6]