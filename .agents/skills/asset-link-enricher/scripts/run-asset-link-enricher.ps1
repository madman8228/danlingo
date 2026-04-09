param(
  [string]$RepoRoot = "d:\06-project\expo_duo",
  [string]$OutFile = ""
)

$ErrorActionPreference = 'Stop'
[Console]::InputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$PSDefaultParameterValues['*:Encoding'] = 'utf8'

$duoxxDir = Join-Path $RepoRoot 'duoxx'
$testTarget = 'src/services/__tests__/lexiconAssetsBundleRehearsal.test.ts'
$diagnosticTarget = 'src/services/__tests__/assetParseDiagnostics.test.ts'
$governanceTarget = 'src/services/__tests__/assetLinkGovernanceRehearsal.test.ts'

function Run-JestTarget {
  param(
    [string]$Target
  )
  $output = cmd /c "npm test -- $Target --runInBand 2>&1" | Out-String
  $exitCode = $LASTEXITCODE
  return @{
    output = $output
    exitCode = $exitCode
  }
}

if (-not (Test-Path (Join-Path $RepoRoot 'asserts'))) {
  throw "Assets directory not found: $RepoRoot\asserts"
}

if (-not (Test-Path $duoxxDir)) {
  throw "duoxx directory not found: $duoxxDir"
}

Push-Location $duoxxDir
try {
  $rehearsalResult = Run-JestTarget -Target $testTarget
  $diagnosticResult = Run-JestTarget -Target $diagnosticTarget
  $governanceResult = Run-JestTarget -Target $governanceTarget
} finally {
  Pop-Location
}

if ($rehearsalResult.exitCode -ne 0) {
  Write-Host $rehearsalResult.output
  throw "Rehearsal test failed."
}

if ($diagnosticResult.exitCode -ne 0) {
  Write-Host $diagnosticResult.output
  throw "Diagnostic test failed."
}

if ($governanceResult.exitCode -ne 0) {
  Write-Host $governanceResult.output
  throw "Governance test failed."
}

$line = $rehearsalResult.output -split "`r?`n" | Where-Object { $_ -match '\[asserts-rehearsal\]' } | Select-Object -Last 1
if (-not $line) {
  Write-Host $rehearsalResult.output
  throw "Cannot find [asserts-rehearsal] summary line in test output."
}

$jsonText = ($line -replace '^.*\[asserts-rehearsal\]\s*', '').Trim()
$summary = $jsonText | ConvertFrom-Json

$sorted = @($summary.fileSummaries | Sort-Object -Property @{Expression='unresolvedRefs';Descending=$true}, @{Expression='skippedBlocks';Descending=$true})
$summary | Add-Member -NotePropertyName sortedByRisk -NotePropertyValue $sorted -Force

$diagLine = $diagnosticResult.output -split "`r?`n" | Where-Object { $_ -match '\[asset-parse-diagnostics\]' } | Select-Object -Last 1
$diagnostics = @()
if ($diagLine) {
  $diagText = ($diagLine -replace '^.*\[asset-parse-diagnostics\]\s*', '').Trim()
  if ($diagText) {
    try {
      $diagnostics = @($diagText | ConvertFrom-Json)
    } catch {
      $diagnostics = @()
    }
  }
}

$governanceLine = $governanceResult.output -split "`r?`n" | Where-Object { $_ -match '\[asset-link-governance\]' } | Select-Object -Last 1
$governance = $null
if ($governanceLine) {
  $governanceText = ($governanceLine -replace '^.*\[asset-link-governance\]\s*', '').Trim()
  if ($governanceText) {
    try {
      $governance = $governanceText | ConvertFrom-Json
    } catch {
      $governance = $null
    }
  }
}

Write-Host "[asset-link-enricher] Summary"
Write-Host ("batchId: {0}" -f $summary.batchId)
Write-Host ("files: {0}, entries: {1}, nodes: {2}, edges: {3}" -f $summary.totalFiles, $summary.totalEntries, $summary.nodesTotal, $summary.edgesTotal)
Write-Host ("unresolvedRefs: {0}, pendingReview: {1}" -f $summary.unresolvedRefs, $summary.pendingReview)
Write-Host "Top files by unresolved/skipped:"
$summary.sortedByRisk | ForEach-Object {
  Write-Host ("- {0}: unresolved={1}, skipped={2}, parsed={3}" -f $_.fileName, $_.unresolvedRefs, $_.skippedBlocks, $_.parsedBlocks)
}

if ($summary.PSObject.Properties.Name -contains 'unresolvedTopByFile') {
  Write-Host "Top unresolved labels by file:"
  foreach ($file in $summary.unresolvedTopByFile) {
    $labels = @($file.topLabels | ForEach-Object { "{0} ({1})" -f $_.label, $_.count }) -join '; '
    Write-Host ("- {0}: {1}" -f $file.fileName, $labels)
  }
}

if ($diagnostics.Count -gt 0) {
  Write-Host "Parser diagnostics by file:"
  foreach ($item in ($diagnostics | Sort-Object -Property @{Expression='skippedBlocks';Descending=$true}, @{Expression='entries';Descending=$true})) {
    $warningCount = @($item.warnings).Count
    $errorCount = @($item.errors).Count
    Write-Host ("- {0}: entries={1}, parsed={2}, skipped={3}, warnings={4}, errors={5}" -f $item.fileName, $item.entries, $item.parsedBlocks, $item.skippedBlocks, $warningCount, $errorCount)
  }
}

if ($null -ne $governance) {
  $failedFiles = @($governance.contract.failedFiles)
  $strategyStats = $governance.patchSuggestions.byStrategy
  $addAliasCount = if ($null -ne $strategyStats -and $null -ne $strategyStats.add_alias) { [int]$strategyStats.add_alias } else { 0 }
  $addRefCount = if ($null -ne $strategyStats -and $null -ne $strategyStats.add_ref) { [int]$strategyStats.add_ref } else { 0 }
  $createNodeCount = if ($null -ne $strategyStats -and $null -ne $strategyStats.create_node) { [int]$strategyStats.create_node } else { 0 }
  Write-Host "Governance contract:"
  Write-Host ("- failed files: {0}" -f ($failedFiles -join ', '))
  Write-Host ("- registry keys: {0} (duplicates: {1})" -f $governance.registry.distinctCanonicalKeys, $governance.registry.duplicateCanonicalKeys)
  Write-Host ("- patch suggestions: total={0}, add_alias={1}, add_ref={2}, create_node={3}" -f `
    $governance.patchSuggestions.total, `
    $addAliasCount, `
    $addRefCount, `
    $createNodeCount)
}

if ($OutFile) {
  $outDir = Split-Path -Path $OutFile -Parent
  if ($outDir -and -not (Test-Path $outDir)) {
    New-Item -Path $outDir -ItemType Directory -Force | Out-Null
  }
  $reportPayload = @{
    summary = $summary
    diagnostics = $diagnostics
    governance = $governance
  }
  $reportPayload | ConvertTo-Json -Depth 10 | Set-Content -Path $OutFile -Encoding utf8
  Write-Host ("Saved summary to {0}" -f $OutFile)
}
