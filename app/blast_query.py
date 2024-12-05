from Bio.Blast.Applications import NcbiblastpCommandline
from io import StringIO
from Bio.Blast import NCBIXML

def blast_query(query_sequence):
    # BLASTP command parameters
    blastp_cline = NcbiblastpCommandline(db="blastp_db_toy/toy_viro3d_seq_db.fas", outfmt=5, num_threads=4)
    
    # Execute BLASTP search with command line wrapper
    stdout, stderr = blastp_cline(stdin=query_sequence, stdout=True, stderr=True)
    
    if stderr:
        print(f"Error occurred: {stderr}")
        return None
    
    # The tool outputs the most information to XML, so need to parse this
    result_handle = StringIO(stdout)
    blast_records = NCBIXML.parse(result_handle)
    
    # Process the data here
    for record in blast_records:
        print(f"Query: {record.query}")
        for alignment in record.alignments:
            for hsp in alignment.hsps:
                print(f"Subject: {alignment.hit_def}, Score: {hsp.score} Positives: {hsp.positives}, gaps: {hsp.gaps}")
    
    return blast_records

seq = 'MSASKEIKSFLWTQSLRRELSGYCSNIKLQVVKDAQALLHGLDFSEVSNVQRLMRKERRDDNDLKRLRDLNQAVNNLVELKSTQQKSILRVGTLTSDDLLILAADLEKLKSKVIRTERPLSAGVYMGNLSSQQLDQRRALLNMIGMSGGNQGARAGRDGVVRVWDVKNAELLNNQFGTMPSLTLACLTKQGQVDLNDAVQALTDLGLIYTAKYPNTSDLDRLTQSHPILNMIDTKKSSLNISGYNFSLGAAVKAGACMLDGGNMLETIKVSPQTMDGILKSILKVKKALGMFISDTPGERNPYENILYKICLSGDGWPYIASRTSITGRAWENTVVDLESDGKPQKADSNNSSKSLQSAGFTAGLTYSQLMTLKDAMLQLDPNAKTWMDIEGRPEDPVEIALYQPSSGCYIHFFREPTDLKQFKQDAKYSHGIDVTDLFATQPGLTSAVIDALPRNMVITCQGSDDIRKLLESQGRKDIKLIDIALSKTDSRKYENAVWDQYKDLCHMHTGVVVEKKKRGGKEEITPHCALMDCIMFDAAVSGGLNTSVLRAVLPRDMVFRTSTPRVVL'