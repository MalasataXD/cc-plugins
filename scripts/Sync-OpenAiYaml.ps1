<#
.SYNOPSIS
Sync every skill's agents/openai.yaml from its SKILL.md frontmatter.

.DESCRIPTION
SKILL.md is the source of truth: `description` becomes `short_description`, and
`disable-model-invocation: true` becomes the Codex policy block that turns
implicit invocation off. An existing display_name is kept; a missing one is
derived from the skill name.

Runs on Windows PowerShell 5.1 and PowerShell 7, so stick to syntax both share.

.EXAMPLE
./scripts/Sync-OpenAiYaml.ps1          # write what changed
./scripts/Sync-OpenAiYaml.ps1 -Check   # list drift, exit 1 if any
#>
#Requires -Version 5.1
[CmdletBinding()]
param([switch]$Check)

$root = Split-Path -Parent $PSScriptRoot
$skills = Join-Path $root 'skills'
$acronyms = @{ tdd = 'TDD'; pr = 'PR'; adr = 'ADR'; api = 'API' }
$smallWords = @('for', 'a', 'an', 'the', 'of', 'to', 'in', 'on', 'with')

# Read the `key: value` pairs between the leading `---` fences.
function Get-Frontmatter([string]$path) {
    $text = Get-Content $path -Raw -Encoding UTF8
    if ($text -notmatch '(?s)^---\r?\n(.*?)\r?\n---') { throw "$path has no frontmatter" }
    $pairs = @{}
    foreach ($line in $Matches[1] -split '\r?\n') {
        $key, $value = $line -split ':', 2
        if ($null -ne $value) { $pairs[$key.Trim()] = $value.Trim() }
    }
    return $pairs
}

# `writing-for-agents` -> `Writing for Agents`, `file-pr` -> `File PR`.
function Get-DisplayName([string]$skillName) {
    $words = $skillName -split '-'
    $out = for ($i = 0; $i -lt $words.Count; $i++) {
        $word = $words[$i]
        if ($acronyms.ContainsKey($word)) { $acronyms[$word] }
        elseif ($i -gt 0 -and $smallWords -contains $word) { $word }
        else { $word.Substring(0, 1).ToUpper() + $word.Substring(1) }
    }
    return $out -join ' '
}

function Get-ExistingDisplayName([string]$yamlPath) {
    if (-not (Test-Path $yamlPath)) { return $null }
    if ((Get-Content $yamlPath -Raw -Encoding UTF8) -match 'display_name:\s*"(.*)"') { return $Matches[1] }
    return $null
}

function Format-Yaml([string]$name, [string]$description, [bool]$userInvoked) {
    $escaped = $description.Replace('"', '\"')
    $lines = @(
        'interface:'
        "  display_name: `"$name`""
        "  short_description: `"$escaped`""
    )
    if ($userInvoked) { $lines += @('policy:', '  allow_implicit_invocation: false') }
    return ($lines -join "`n") + "`n"
}

$drift = @()
foreach ($skillMd in Get-ChildItem $skills -Filter SKILL.md -Recurse -Depth 2 | Sort-Object FullName) {
    $meta = Get-Frontmatter $skillMd.FullName
    $yamlPath = Join-Path (Join-Path $skillMd.DirectoryName 'agents') 'openai.yaml'
    $name = Get-ExistingDisplayName $yamlPath
    if (-not $name) { $name = Get-DisplayName $meta['name'] }
    $userInvoked = "$($meta['disable-model-invocation'])".ToLower() -eq 'true'
    $wanted = Format-Yaml $name $meta['description'] $userInvoked
    $current = if (Test-Path $yamlPath) { (Get-Content $yamlPath -Raw -Encoding UTF8).Replace("`r`n", "`n") } else { '' }
    if ($current -eq $wanted) { continue }

    $drift += $skillMd.DirectoryName.Substring($root.Length + 1)
    if (-not $Check) {
        New-Item -ItemType Directory -Force (Split-Path $yamlPath) | Out-Null
        [System.IO.File]::WriteAllText($yamlPath, $wanted, [System.Text.UTF8Encoding]::new($false))
    }
}

$verb = if ($Check) { 'out of sync' } else { 'updated' }
foreach ($path in $drift) { Write-Output "${verb}: $path" }
if ($drift.Count -eq 0) { Write-Output 'all openai.yaml files in sync' }
exit $(if ($Check -and $drift.Count -gt 0) { 1 } else { 0 })
