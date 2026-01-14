Add-Type -AssemblyName "System.IO.Compression.FileSystem"
$zip = [System.IO.Compression.ZipFile]::OpenRead("E:\The Human Algorithm\T2\agent\Parameters_The_Umbrella.docx")
$entry = $zip.Entries | Where-Object { $_.FullName -eq "word/document.xml" }
$stream = $entry.Open()
$reader = New-Object System.IO.StreamReader($stream)
$xml = $reader.ReadToEnd()
$stream.Close()
$zip.Dispose()

# Simple dirty way to strip XML tags to get some readable text
$text = $xml -replace "<[^>]+>", " "
[System.IO.File]::WriteAllText("e:\The Human Algorithm\T2\agent\extracted_umbrella.txt", $text, [System.Text.Encoding]::UTF8)
