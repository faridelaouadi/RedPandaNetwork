from testing import *
import asyncio

filepaths = [
    './static/uploads/1.jpeg',
    './static/uploads/f1.jpeg',
    './static/uploads/f2.jpeg'
]

results = asyncio.run(main(filepaths))
print(results)