from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


class ContextValidator:
    """
    Component for validating that responses are properly grounded in context
    """
    
    def __init__(self):
        # Initialize any required resources for context validation
        pass
    
    def validate_global_context(self, query: str, retrieved_chunks: List[Dict[str, Any]], response: str) -> Dict[str, Any]:
        """
        Validate that a response for a global query is properly grounded in retrieved context
        """
        validation_result = {
            "is_valid": True,
            "issues": [],
            "confidence_score": 1.0
        }
        
        # Check if response contains information from retrieved chunks
        response_lower = response.lower()
        has_supporting_evidence = False
        
        for chunk in retrieved_chunks:
            chunk_content = chunk.get("content", "").lower()
            if self._text_overlaps(response_lower, chunk_content):
                has_supporting_evidence = True
                break
        
        if not has_supporting_evidence:
            validation_result["is_valid"] = False
            validation_result["issues"].append("Response does not appear to be grounded in retrieved context")
            validation_result["confidence_score"] = 0.0
        
        # Check for hallucinations (mentioning information not in context)
        hallucinations = self._check_for_hallucinations(response, retrieved_chunks)
        if hallucinations:
            validation_result["is_valid"] = False
            validation_result["issues"].extend(hallucinations)
            validation_result["confidence_score"] = 0.0
        
        logger.info(f"Global context validation: {validation_result['is_valid']} - {validation_result['issues']}")
        return validation_result
    
    def validate_selected_text_context(self, query: str, selected_text: str, response: str) -> Dict[str, Any]:
        """
        Validate that a response for a selected-text query only references the provided text
        """
        validation_result = {
            "is_valid": True,
            "issues": [],
            "confidence_score": 1.0
        }
        
        # Check if response contains information from outside the selected text
        response_lower = response.lower()
        selected_text_lower = selected_text.lower()
        
        if not self._text_overlaps(response_lower, selected_text_lower):
            # If there's no overlap, check if response is still related to selected text
            if not self._is_related_to_text(query, selected_text, response):
                validation_result["is_valid"] = False
                validation_result["issues"].append("Response does not appear to be related to selected text")
                validation_result["confidence_score"] = 0.0
        else:
            # Check for content that's not in the selected text
            potential_hallucinations = self._find_content_not_in_selected_text(response, selected_text)
            if potential_hallucinations:
                validation_result["is_valid"] = False
                validation_result["issues"].extend([
                    f"Response contains information not found in selected text: {halluc}"
                    for halluc in potential_hallucinations
                ])
                validation_result["confidence_score"] = 0.0
        
        logger.info(f"Selected text context validation: {validation_result['is_valid']} - {validation_result['issues']}")
        return validation_result
    
    def _text_overlaps(self, text1: str, text2: str, threshold: float = 0.1) -> bool:
        """
        Check if two texts have significant overlap
        """
        # Simple word overlap check
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        if not words1 or not words2:
            return False
        
        common_words = words1.intersection(words2)
        overlap_ratio = len(common_words) / min(len(words1), len(words2))
        
        return overlap_ratio >= threshold
    
    def _check_for_hallucinations(self, response: str, retrieved_chunks: List[Dict[str, Any]]) -> List[str]:
        """
        Check if response contains information not present in retrieved chunks
        """
        hallucinations = []
        
        # Combine all retrieved content
        all_retrieved_content = " ".join([chunk.get("content", "") for chunk in retrieved_chunks])
        all_retrieved_content_lower = all_retrieved_content.lower()
        
        # This is a simplified check - in practice, you'd want more sophisticated semantic analysis
        response_sentences = response.split('. ')
        
        for sentence in response_sentences:
            sentence_lower = sentence.lower().strip()
            if sentence_lower and sentence_lower not in all_retrieved_content_lower:
                # Check if it's a general statement that doesn't need grounding
                if not self._is_general_statement(sentence_lower):
                    hallucinations.append(sentence)
        
        return hallucinations
    
    def _is_general_statement(self, text: str) -> bool:
        """
        Check if text is a general statement that doesn't require specific grounding
        """
        general_indicators = [
            "the", "is", "are", "was", "were", "a", "an", "and", "or", "but",
            "in", "on", "at", "to", "for", "of", "with", "by", "it", "that",
            "this", "these", "those", "i", "you", "we", "they", "he", "she",
            "can", "could", "would", "should", "may", "might", "must"
        ]
        
        # If the text is mostly general words, it might be a general statement
        words = text.split()
        if not words:
            return True
        
        general_word_count = sum(1 for word in words if word in general_indicators)
        return general_word_count / len(words) > 0.6
    
    def _find_content_not_in_selected_text(self, response: str, selected_text: str) -> List[str]:
        """
        Find parts of the response that are not in the selected text
        """
        not_found_parts = []
        
        # Split response into sentences
        sentences = response.split('. ')
        
        selected_text_lower = selected_text.lower()
        
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            if sentence_lower and sentence_lower not in selected_text_lower:
                # Check if it's just a general statement
                if not self._is_general_statement(sentence_lower):
                    not_found_parts.append(sentence)
        
        return not_found_parts
    
    def _is_related_to_text(self, query: str, selected_text: str, response: str) -> bool:
        """
        Check if response is related to the selected text given the query
        """
        # This is a simplified check - in practice, you'd use semantic similarity
        query_lower = query.lower()
        selected_text_lower = selected_text.lower()
        response_lower = response.lower()
        
        # Check if response addresses the query in the context of selected text
        # This is a basic implementation - real implementation would use embeddings
        query_in_response = any(word in response_lower for word in query_lower.split() if len(word) > 3)
        text_in_response = any(word in response_lower for word in selected_text_lower.split() if len(word) > 3)
        
        return query_in_response or text_in_response