module Main where

import Database.PostgreSQL.Simple
import System.IO
import Analysis

main :: IO ()
main = do
    withFile "../password.txt" ReadMode (\handle -> do
        contents <- hGetContents handle
        connection <- connectPostgreSQL $ "host='localhost' port=7538 user=postgres pass=" ++ password
        return connection
        )
    print $ suggestedAction 7 [4, 3, 5, 6]